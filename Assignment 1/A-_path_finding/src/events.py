import pygame as pg
import sys
import math

from src.config import BOARD_SIZE, GRID_SIZE
from src.types import CellMark, HeuristicType, Mode


def handle_keydown(self, event):
    """
    Xử lý sự kiện nhấn phím cho các hành động cụ thể.

    Tham số:
        event (pg.event.Event): Sự kiện nhấn phím từ người dùng.
    """
    if event.key == pg.K_ESCAPE:
        self.quit()  # Thoát chương trình
    elif event.key == pg.K_RIGHT:
        self.step += 1  # Tăng bước
        self.slider.set_value(self.step)  # Cập nhật thanh trượt
    elif event.key == pg.K_LEFT:
        self.step -= 1  # Giảm bước
        self.slider.set_value(self.step)  # Cập nhật thanh trượt
    elif event.key == pg.K_e:
        self.autoAnimation = not self.autoAnimation # toggle auto animation
    elif event.key == pg.K_r:
        self.reset()  # Reset lưới
    elif event.key == pg.K_m:
        self.mode = Mode.Cost if self.mode == Mode.Arrow else Mode.Arrow
        # Chuyển đổi chế độ hiển thị giữa Cost và Arrow
    elif event.key == pg.K_h:
        self.heuristic = HeuristicType((self.heuristic.value + 1) % len(HeuristicType))
        
    if not event.key == pg.K_e:
        if (self.autoAnimation):
            self.autoAnimation = False
                    


def start_drag(self):
    """
    Bắt đầu thao tác kéo bằng cách bật/tắt loại ô ban đầu và thiết lập điều kiện kéo.
    """
    mouse_x, mouse_y = pg.mouse.get_pos()
    self.mouse_held = True
    self.grid.toggled_cells.clear()  # Xóa các ô đã được kéo từ lần kéo trước

    # Nếu chuột trên thanh trượt, bắt đầu kéo thanh trượt
    if self.slider.on_slider(mouse_x, mouse_y):
        self.slider.is_dragging = True
        self.slider.handle_drag(mouse_x, self.update_step)
        return

    # Tính toán vị trí ô dựa trên tọa độ chuột
    pos_x, pos_y = (
        mouse_x // (BOARD_SIZE // GRID_SIZE),
        mouse_y // (BOARD_SIZE // GRID_SIZE),
    )

    if (pos_x >= GRID_SIZE) or (pos_y >= GRID_SIZE):
        return

    cell = self.grid.at((pos_x, pos_y))
    if cell:
        # Nếu là ô bắt đầu hoặc ô kết thúc, set trạng thái ô tương ứng là đang bị kéo
        if cell.is_start():
            self.grid.dragging_start = True
        elif cell.is_end():
            self.grid.dragging_end = True
        else:
            # Nếu không phải ô bắt đầu hoặc ô kết thúc, thay đổi loại ô và thêm ô đó vào danh sách ô đã được kéo
            # Để khi kéo chuột lại ô đó thì sẽ không bị thay đổi
            cell.toggle_type()
            self.grid.drag_cell_type = cell.type
            self.grid.toggled_cells.add((pos_x, pos_y))


def end_drag(self):
    """
    Kết thúc thao tác kéo và xóa dữ liệu theo dõi.
    """
    self.mouse_held = False
    self.slider.is_dragging = False
    self.grid.drag_cell_type = None
    self.grid.dragging_start = False
    self.grid.dragging_end = False
    self.grid.toggled_cells.clear()


def drag_toggle(self):
    """
    Thay đổi loại ô khi di chuyển chuột trong khi giữ nút kéo, hoặc di chuyển ô bắt đầu/kết thúc.
    """
    mouse_x, mouse_y = pg.mouse.get_pos()

    # Nếu đang kéo thanh trượt, xử lý kéo thanh trượt
    if self.slider.is_dragging:
        self.slider.handle_drag(mouse_x, self.update_step)
        return

    pos_x = mouse_x // (BOARD_SIZE // GRID_SIZE)
    pos_y = mouse_y // (BOARD_SIZE // GRID_SIZE)

    if (pos_x >= GRID_SIZE) or (pos_y >= GRID_SIZE):
        return

    cell = self.grid.at((pos_x, pos_y))

    # Nếu đang kéo ô bắt đầu hoặc ô kết thúc, di chuyển chúng đến vị trí mới
    if self.grid.dragging_start:
        self.grid.get_start().cost = math.inf
        self.grid.get_start().mark = CellMark.No  # Xóa ô bắt đầu trước đó
        self.grid.set_start((pos_x, pos_y))  # Di chuyển ô bắt đầu đến vị trí mới
    elif self.grid.dragging_end:
        self.grid.get_end().mark = CellMark.No  # Xóa ô kết thúc trước đó
        self.grid.set_end((pos_x, pos_y))  # Di chuyển ô kết thúc đến vị trí mới
    elif (pos_x, pos_y) not in self.grid.toggled_cells and cell:
        # Thay đổi loại ô nếu là ô thường và chưa bị kéo trước đó
        if cell.type != self.grid.drag_cell_type:
            cell.toggle_type()
            self.grid.toggled_cells.add((pos_x, pos_y))


def quit(self):
    """
    Thoát khỏi ứng dụng, dừng Pygame và đóng chương trình.
    """
    pg.quit()
    sys.exit()
