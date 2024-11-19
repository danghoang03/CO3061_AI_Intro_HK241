from __future__ import annotations  # For forward reference of CellGrid

import math

import pygame as pg

from src.config import (
    CELL_GAP,
    CELL_SIZE,
    MARGIN,
)
from src.types import ArrowDirection, CellMark, CellType
from src.ui import Arrow
from src.utils import add_point


class Cell:
    """
    Lớp đại diện cho một ô trong lưới với các thuộc tính và trạng thái.

    Attributes:
        type (CellType): Loại ô (ví dụ: trống hoặc vật cản).
        count (float): Trọng số (đặt ban đầu là vô cùng).
        priority (float): Độ ưu tiên trong thuật toán A* (đặt ban đầu là vô cùng).
        hidden (float): Trọng số (ẩn) của ô.
        mark (CellMark): Bắt đầu, kết thúc, hoặc không có.
        path_from (Cell | None): Ô trước đó.
        arrow (Arrow): Hướng mũi tên chỉ về ô trước đó trong đường đi.
        pos (tuple[int, int]): Vị trí của ô trong lưới.
    """

    def __init__(self, type=CellType.Empty, pos=None):
        self.type = type
        self.cost = math.inf
        self.heuristic = math.inf
        self.mark = CellMark.No
        self.path_from: None | Cell = None
        self.arrow: Arrow = None
        self.pos: None | tuple[int, int] = pos
        self.hidden = math.inf
        self.is_current = False
        self.is_next = False

    def __lt__(self, other):
        """
        So sánh hai ô dựa trên số bước kể từ ô bắt đầu (count)
        để hỗ trợ cho hàng đợi ưu tiên.
        """
        return self.hidden > other.hidden

    def is_start(self):
        return self.mark == CellMark.Start

    def is_end(self):
        return self.mark == CellMark.End

    def toggle_type(self):
        """
        Chuyển đổi loại ô giữa Trống và Tường.
        Dùng khi người dùng kéo chuột qua lưới.
        """
        self.type = CellType.Wall if self.type == CellType.Empty else CellType.Empty

    def update_cell(self, count: int, path_from: Cell, heuristic: float):
        """
        Cập nhật ô với số bước kể từ ô bắt đầu,
        độ ưu tiên và ô trước đó trong đường đi.
        Parameters:
            cost (int): Giá trị đếm cho ô.
            path_from (Cell): Ô trước đó trong đường đi đến ô hiện tại.
            heuristic (float): Giá trị của hàm lượng giá tại ô
        """
        self.cost = count
        self.path_from = path_from
        self.heuristic = heuristic

        if path_from is not None:
            if path_from.pos[0] < self.pos[0]:
                self.arrow = Arrow(ArrowDirection.Left)
            elif path_from.pos[0] > self.pos[0]:
                self.arrow = Arrow(ArrowDirection.Right)
            elif path_from.pos[1] < self.pos[1]:
                self.arrow = Arrow(ArrowDirection.Up)
            elif path_from.pos[1] > self.pos[1]:
                self.arrow = Arrow(ArrowDirection.Down)


class GridMetrics:
    """
    Lớp tính toán kích thước và vị trí của các ô trong lưới.

    Attributes:
        area (tuple[int, int, int, int]): Định nghĩa vùng (trái, trên, phải, dưới) của lưới.
        left (int): Tọa độ trái của vùng lưới có khoảng cách.
        top (int): Tọa độ trên của vùng lưới có khoảng cách.
        width (int): Chiều rộng của vùng lưới điều chỉnh theo khoảng cách.
        height (int): Chiều cao của vùng lưới điều chỉnh theo khoảng cách.
    """

    def __init__(self, area: tuple[int, int, int, int], grid: CellGrid):
        self.area = area
        self.left = area[0] + MARGIN
        self.top = area[1] + MARGIN
        self.width = area[2] - area[0] - 2 * MARGIN
        self.height = area[3] - area[1] - 2 * MARGIN

        self.pos_x, self.pos_y = grid.get_size()

    def cell_rect(self, pos: tuple[int, int]) -> pg.Rect:
        """
        Lấy hình chữ nhật (pygame.Rect) đại diện cho một ô tại vị trí `pos`.

        Parameters:
            pos (tuple[int, int]): Vị trí của ô trong lưới.

        Returns:
            pg.Rect: Hình chữ nhật đại diện cho ô tại `pos`.
        """
        return pg.Rect(
            self.left + pos[0] * (CELL_SIZE + CELL_GAP),
            self.top + pos[1] * (CELL_SIZE + CELL_GAP),
            CELL_SIZE,
            CELL_SIZE,
        )

    def cell_center(self, pos: tuple[int, int]) -> tuple[int, int]:
        """
        Lấy tọa độ trung tâm của ô tại `pos`.

        Parameters:
            pos (tuple[int, int]): Vị trí của ô trong lưới.

        Returns:
            tuple[int, int]: Tọa độ trung tâm của ô tại `pos`.
        """
        rect = self.cell_rect(pos)
        return rect.center


class CellGrid:
    """
    Lớp đại diện cho toàn bộ lưới ô và quản lý các chức năng như
    thiết lập ô bắt đầu, ô kết thúc, lấy các ô lân cận, và các thao tác với lưới.

    Attributes:
        grid (list[list[Cell]]): Ma trận các ô trong lưới.
        metrics (GridMetrics): Các thông số về kích thước và vị trí cho lưới.
    """

    def __init__(
        self,
        area: tuple[int, int, int, int],
        grid: list[list[Cell]],
        start=None,
        end=None,
    ):
        self.grid = grid
        self.set_start(start)
        self.set_end(end)
        self.metrics = GridMetrics(area, self)

        self.toggled_cells = set()
        # Tập hợp chứa các ô đã được đổi khi người dùng kéo chuột
        self.drag_cell_type = None
        # Loại của ô khi bắt đầu kéo chuột, ví dụ khi bắt đầu ở loại trống (Empty)
        # thì các ô bị chuột di qua sẽ chuyển thành vật cản (Wall)

        self.dragging_start = False
        self.dragging_end = False
        # Dùng để xác định ô được kéo có phải ô bắt đâu hay kết thúc không

    def get_size(self) -> tuple[int, int]:
        """
        Trả về kích thước của lưới

        Returns:
            tuple[int, int]: Kích thước của lưới (zero-index).
        """
        return (len(self.grid), len(self.grid[0]))  # Using a tuple

    def at(self, pos: tuple[int, int]) -> Cell:
        """
        Trả về ô tại vị trí `pos` trong lưới.

        Parameters:
            pos (tuple[int, int]): Vị trí của ô.

        Returns:
            Cell: Ô tại vị trí `pos`.
        """
        return self.grid[pos[0]][pos[1]]

    def clear_count(self) -> None:
        """
        Reset các giá trị của ô về ban đầu
        """
        for row in self.grid:
            for cell in row:
                cell.cost = math.inf if cell.mark != CellMark.Start else 0
                cell.hidden = math.inf if cell.mark != CellMark.Start else 0
                cell.path_from = None
                cell.arrow = None
                cell.is_current = False
                cell.is_next = False

    def set_start(self, pos: tuple[int, int]) -> None:
        """Đặt các gái trị của ô bắt đầu."""
        self.start = pos
        self.at(pos).mark = CellMark.Start
        self.at(pos).cost = 0
        self.at(pos).hidden = 0

    def set_end(self, pos: tuple[int, int]) -> None:
        """Đặt các giá trị của ô kết thúc"""
        self.end = pos
        self.at(pos).mark = CellMark.End

    def get_start(self) -> Cell:
        """Lấy ô bắt đầu"""
        return self.grid[self.start[0]][self.start[1]]

    def get_end(self) -> Cell:
        """Lấy ô kết thúc"""
        return self.grid[self.end[0]][self.end[1]]

    def get_neighbors(self, pos: tuple[int, int]) -> list[Cell]:
        """
        Lấy các ô lân cận của ô tại vị trí `pos`.

        Parameters:
            pos (tuple[int, int]): Vị trí của ô.

        Returns:
            list[Cell]: Danh sách các ô lân cận.
        """
        neighbors = []
        offsets = (
            [(0, -1), (-1, 0), (0, 1), (1, 0)]
            if (pos[0] + pos[1]) % 2
            else [(1, 0), (0, 1), (-1, 0), (0, -1)]
        )

        for offset in offsets:
            ncell_pos = add_point(pos, offset)
            if 0 <= ncell_pos[0] < len(self.grid) and 0 <= ncell_pos[1] < len(
                self.grid[0]
            ):
                ncell = self.at(ncell_pos)
                if ncell.type == CellType.Empty:
                    neighbors.append(ncell)
        return neighbors
