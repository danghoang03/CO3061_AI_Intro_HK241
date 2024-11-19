import math
import pygame as pg
from src.config import (
    ARROW_COLOR,
    ARROW_SIZE,
    BOARD_SIZE,
    CELL_COLOR_EMPTY,
    CELL_CURRENT_COLOR,
    CELL_NEXT_COLOR,
    CELL_SIZE,
    FONT_COLOR,
    LOGGER_FONT_SIZE,
    MARGIN,
    SCREEN_HEIGHT,
    SLIDER_BAR_COLOR,
    SLIDER_THUMB_COLOR,
    SLIDER_THUMB_SIZE,
)
from src.types import ArrowDirection


class Slider:
    """
    Lớp đại diện cho thanh trượt số bước.

    Attributes:
        circle_x (float): Vị trí x của nút kéo trên của sổ.
        value (int): Giá trị hiện tại của thanh trượt đi từ 0 -> số bước tối đa
        is_dragging (bool): Trạng thái đang kéo của nút.
        sliderRect (pg.Rect): Khu vực chứa thanh trượt.
        intervals (int): Số khoảng chia trên thanh trượt, bằng với số bước tối đa.
        interval_width (float): Độ rộng của mỗi khoảng trên thanh trượt.
    """

    def __init__(self, x, y, w, h, intervals=100):
        self.circle_x = x
        self.value = 0
        self.is_dragging = False
        self.sliderRect = pg.Rect(x, y, w, h)
        self.intervals = intervals
        self.interval_width = w / intervals

    def draw(self, screen):
        """
        Vẽ thanh trượt và nút kéo lên màn hình dựa vào giá trị hiện tại.
        """
        pg.draw.rect(screen, SLIDER_BAR_COLOR, self.sliderRect)

        self.circle_x = (
            self.sliderRect.x + (self.value / self.intervals) * self.sliderRect.w
        )

        pg.draw.circle(
            screen,
            SLIDER_THUMB_COLOR,
            (int(self.circle_x), int(self.sliderRect.h / 2 + self.sliderRect.y)),
            SLIDER_THUMB_SIZE,
        )

    def set_intervals(self, intervals):
        """
        Đặt số khoản của của thanh trượt.
        """
        self.intervals = intervals
        self.interval_width = self.sliderRect.w / intervals

    def get_value(self):
        return self.value

    def set_value(self, num):
        self.value = max(
            0, min(num, self.intervals)
        )  # Ensure the value is within 0 to intervals
        self.circle_x = (
            self.sliderRect.x + (self.value / self.intervals) * self.sliderRect.w
        )

    def update_value(self, x):
        """
        Cập nhật giá trị của thanh trượt dựa trên vị trí x của nút kéo.
        Dùng để cập nhật giá trị khi nút kéo được kéo.
        Dùng trong hàm handle_drag.
        """
        if x < self.sliderRect.x:
            self.value = 0
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.value = self.intervals
        else:
            self.value = int(
                (x - self.sliderRect.x) / float(self.sliderRect.w) * self.intervals
            )

    def snap_to_interval(self, x):
        """
        Làm tròn vị trí x của nút kéo đến điểm gần nhất trong các khoảng.
        """
        relative_x = x - self.sliderRect.x
        snapped_x = round(relative_x / self.interval_width) * self.interval_width
        return int(self.sliderRect.x + snapped_x)

    def on_slider(self, x, y):
        """
        Kiểm tra xem vị trí x, y có nằm trong thanh trượt hoặc nút kéo.
        """
        return (
            self.on_slider_hold(x, y)
            or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w
            and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h
        )

    def on_slider_hold(self, x, y):
        """Kiểm tra xem nút kéo có đang bị giữ không."""
        return (
            (x - self.circle_x) ** 2
            + (y - (self.sliderRect.y + self.sliderRect.h / 2)) ** 2
        ) <= SLIDER_THUMB_SIZE**2

    def handle_drag(self, x, event=None):
        """Xử lý việc kéo nút, cập nhật giá trị dựa vào vị trí x"""
        self.circle_x = self.snap_to_interval(x)
        self.update_value(self.circle_x)

        if event is not None and callable(event):
            event(self.value)


class Arrow:
    """
    Lớp đại diện cho mũi tên chỉ hướng trong một ô trên lưới.

    Attributes:
        direction (ArrowDirection): Hướng của mũi tên (Right, Left, Up, Down).
    """

    def __init__(self, direction: ArrowDirection) -> None:
        self.direction = direction

    def draw_arrow(self, surface, cell_center):
        """
        Vẽ mũi tên bên trong ô theo hướng `direction`.
        """
        half_size = CELL_SIZE / 4
        if self.direction == ArrowDirection.Right:
            arrow_start = (cell_center[0] - half_size, cell_center[1])
            arrow_end = (cell_center[0] + half_size, cell_center[1])
        elif self.direction == ArrowDirection.Left:
            arrow_start = (cell_center[0] + half_size, cell_center[1])
            arrow_end = (cell_center[0] - half_size, cell_center[1])
        elif self.direction == ArrowDirection.Up:
            arrow_start = (cell_center[0], cell_center[1] + half_size)
            arrow_end = (cell_center[0], cell_center[1] - half_size)
        elif self.direction == ArrowDirection.Down:
            arrow_start = (cell_center[0], cell_center[1] - half_size)
            arrow_end = (cell_center[0], cell_center[1] + half_size)
        else:
            return

        pg.draw.line(surface, ARROW_COLOR, arrow_start, arrow_end, ARROW_SIZE)

        angle = math.atan2(arrow_end[1] - arrow_start[1], arrow_end[0] - arrow_start[0])
        arrow_length = 8
        arrow_angle = math.pi / 6

        left_point = (
            arrow_end[0] - arrow_length * math.cos(angle + arrow_angle),
            arrow_end[1] - arrow_length * math.sin(angle + arrow_angle),
        )
        right_point = (
            arrow_end[0] - arrow_length * math.cos(angle - arrow_angle),
            arrow_end[1] - arrow_length * math.sin(angle - arrow_angle),
        )

        pg.draw.polygon(surface, ARROW_COLOR, [arrow_end, left_point, right_point])


class Logger:
    """
    Lớp đại diện cho cửa sổ thông tin.

    Attributes:
        queue_items (PriorityQueue): Priority queue hiện tại.
        curent_cell = Cell: Ô hiện tại đang được khám phá
        evaluations_count = int: Số ô đã được khám phá

    """

    HEADER_TEXT = """___Instruction___:
Left - Decrease step
Right - Increase step
E - Auto increate step
R - create a new maze
M - change display mode
H - change heuristic
Esc - Exit"""

    def __init__(self):
        self.queue_items = None
        self.current_cell = None
        self.heuristic = None
        self.evaluations_count = 0
        self.font = pg.font.SysFont(pg.font.get_default_font(), LOGGER_FONT_SIZE)

    def update(self, queue_items, current, count, heuristic):
        """Cập nhật giá trị của logger

        Args:
            queue_items (list[(Priority, Cell)]): Priority Queue dưới dạng danh sách
            current (Cell): Cell hiện tại đang được khám phá
            count (int): Số ô đa được khám phá
        """
        self.current_cell = current
        self.queue_items = queue_items
        self.evaluations_count = count
        self.heuristic = heuristic

    def draw_queue(self, surface: pg.Surface):
        """Vẽ Priority hiện tại lên logger"""
        surface.blit(
            self.font.render("Priority Queue:", True, FONT_COLOR),
            (
                BOARD_SIZE + MARGIN,
                MARGIN + 20 + LOGGER_FONT_SIZE * 3,
            ),
        )

        for i, (_, cell) in enumerate(self.queue_items):
            if i >= 20:  # Giới hạn số dòng có thể hiển thị là 20
                break

            color = CELL_NEXT_COLOR if i == 0 else FONT_COLOR
            # Giá trị đầu tiên trong Priority Queue (ô tiếp theo được khám phá) sẽ được tô màu khác

            text = self.font.render(
                f"Priority: {cell.cost} + {round(cell.heuristic, 2)}, Position: {cell.pos}",
                True,
                color,
            )
            surface.blit(
                text,
                (BOARD_SIZE + MARGIN, MARGIN + 20 + (i + 4) * LOGGER_FONT_SIZE),
            )

    def draw_instruction(self, surface: pg.Surface):
        """Vẽ các hướng dẫn"""
        header_lines = Logger.HEADER_TEXT.splitlines()
        for i, line in enumerate(header_lines):
            text_surface = self.font.render(line, True, FONT_COLOR)

            surface.blit(
                text_surface,
                (BOARD_SIZE + MARGIN, BOARD_SIZE - 95 + i * LOGGER_FONT_SIZE),
            )

    def draw_current(self, surface: pg.Surface):
        """Vẽ ô đang được khám phá và số lượng ô đã được khám phá"""
        surface.blit(
            self.font.render(
                f"Evaluation count: {self.evaluations_count}",
                1,
                FONT_COLOR,
            ),
            (BOARD_SIZE + MARGIN, MARGIN + 10),
        )
        surface.blit(
            self.font.render(
                f"Heuristic func: {self.heuristic.name}",
                1,
                FONT_COLOR,
            ),
            (BOARD_SIZE + MARGIN, MARGIN + 10 + LOGGER_FONT_SIZE),
        )
        surface.blit(
            self.font.render(
                f"Current: {self.current_cell.cost} + {round(self.current_cell.heuristic,2)}, Position: {self.current_cell.pos}",
                True,
                CELL_CURRENT_COLOR,
            ),
            (BOARD_SIZE + MARGIN, MARGIN + 10 + LOGGER_FONT_SIZE * 2),
        )

    def draw_log(self, surface: pg.Surface):
        """
        Vẽ các thông tin lên logger
        """
        pg.draw.rect(
            surface,
            CELL_COLOR_EMPTY,
            (BOARD_SIZE, MARGIN, 300 - MARGIN, SCREEN_HEIGHT - MARGIN * 2),
        )  # Vẽ background
        self.draw_instruction(surface)

        if self.queue_items is None:
            return

        self.draw_current(surface)
        self.draw_queue(surface)

        pg.display.update()
