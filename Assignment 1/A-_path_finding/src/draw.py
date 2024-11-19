from ast import Dict
import math
import pygame as pg

from src.config import (
    CELL_COLOR_EMPTY,
    CELL_COLOR_WALL,
    CELL_CURRENT_COLOR,
    CELL_NEXT_COLOR,
    FONT_COLOR,
    FONT_SIZE,
    PATH_LINE_WIDTH,
)
from src.types import CellMark, CellType, Mode
from src.grid import CellGrid


def draw_board(surface: pg.Surface, grid: CellGrid, area: pg.Rect, mode: Mode):
    """
    Hàm vẽ toàn bộ lưới lên bề mặt Pygame, với màu sắc của các ô,
    các dấu hiệu đặc biệt, chi phí, và mũi tên chỉ hướng.

    Parameters:
        surface (pg.Surface): Bề mặt nơi lưới sẽ được vẽ.
        grid (CellGrid): Đối tượng lưới chứa các ô cần vẽ.
        area (pg.Rect): Khu vực trong bề mặt để vẽ lưới.
        mode (Mode): Chế độ hiển thị (Cost hoặc Arrow) để hiển thị chi phí hoặc mũi tên.

    Returns:
        None
    """
    cell_font = pg.font.SysFont(pg.font.get_default_font(), FONT_SIZE)  # Font chữ

    pg.draw.rect(surface, (0, 0, 0), area)  # Màu nền
    metrics = grid.metrics  # Lấy thông số lưới

    colors: Dict[CellType, tuple[int, int, int]] = {
        CellType.Empty: CELL_COLOR_EMPTY,
        CellType.Wall: CELL_COLOR_WALL,
    }  # Màu sắc của các ô dựa vào loại ô: trống hoặc vật cản

    marks: Dict[CellMark, tuple[int, int, int]] = {
        CellMark.Start: (0, 255, 0),
        CellMark.End: (255, 0, 0),
    }  # Màu sắc của các ô đặc biệt: ô bắt đầu và ô kết thúc

    for y in range(0, metrics.pos_y):
        # Duyệt qua các hàng
        for x in range(0, metrics.pos_x):
            # Duyệt qua các cột
            cell = grid.at([x, y])  # Lấy ô tại tọa độ [x, y]

            cell_rect = metrics.cell_rect([x, y])  # Thông số ô
            cell_center = metrics.cell_center([x, y])  # Tâm của ô

            pg.draw.rect(
                surface, colors.get(cell.type, (0, 255, 0)), cell_rect
            )  # Vẽ ô với màu tương ứng với loại ô: trống hoặc vật cản

            if mode == Mode.Cost and cell.cost != math.inf:
                # Nếu chế độ hiển thị là Cost và ô có chi phí khác vô cực
                # thì vẽ chi phí lên tâm của ô

                count_text = cell_font.render(
                    str(round(cell.cost + cell.heuristic, 2)), True, FONT_COLOR
                )

                cell_x, cell_y, cell_width, cell_height = cell_rect
                text_width, text_height = count_text.get_rect().size

                text_x = cell_x + (cell_width - text_width) / 2
                text_y = cell_y + (cell_height - text_height) / 2

                surface.blit(count_text, (text_x, text_y))

            if mode == Mode.Arrow and cell.path_from is not None:
                # Nếu chế độ hiển thị là Arrow và ô đó không phải là ô bắt đầu
                # thì vẽ mũi tên từ ô hiện tại đến ô trước đó
                cell.arrow.draw_arrow(surface, cell_center)

            mark = marks.get(cell.mark, None)
            if mark is not None:
                # Nếu ô đó là ô bắt đầu hoặc ô kết thúc
                # thì tô màu cho ô đó với màu tương ứng
                pg.draw.rect(surface, mark, cell_rect)

            if cell.is_current:
                pg.draw.rect(surface, CELL_CURRENT_COLOR, cell_rect, PATH_LINE_WIDTH)

            if cell.is_next:
                pg.draw.rect(surface, CELL_NEXT_COLOR, cell_rect, PATH_LINE_WIDTH)


def draw_path(surface: pg.Surface, grid: CellGrid, path: list[tuple[int, int]]):
    """
    Hàm vẽ đường đi từ ô bắt đầu đến ô kết thúc trên bề mặt Pygame.

    Parameters:
        surface (pg.Surface): Bề mặt nơi đường đi sẽ được vẽ.
        grid (CellGrid): Đối tượng lưới chứa các ô.
        path (list[tuple[int, int]]): Danh sách các tọa độ của các ô trên đường đi từ ô bắt đầu đến ô kết thúc.

    Returns:
        None
    """
    metrics = grid.metrics
    for i in range(0, len(path) - 1):
        # Duyệt qua các ô và vẽ đường đi từ tâm ô này đến ô tiếp theo
        ctr_a = metrics.cell_center(path[i])
        ctr_b = metrics.cell_center(path[i + 1])
        pg.draw.line(surface, (120, 220, 0), ctr_a, ctr_b, PATH_LINE_WIDTH)
