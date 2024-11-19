import pygame as pg
import time

from src.a_star import a_star, a_star_pure, backtrack_to_start
from src.config import (
    AUTO_MODE,
    WRITE_TEST,
    WRITE_PATH,
    TESTCASE_NAME,
    BOARD_SIZE,
    GAME_TITLE,
    GRID_SIZE,
    INPUT_FILE_PATH,
    OUT_FILE_PATH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLIDER_HEIGHT,
    SLIDER_WIDTH,
)
from src.draw import draw_board, draw_path
from src.events import drag_toggle, end_drag, handle_keydown, quit, start_drag
from src.grid import CellGrid
from src.types import HeuristicType, Mode
from src.ui import Logger, Slider
from src.utils import read_input, write_path_to_file
from src.map_generation import gen_grid, auto_gen_grid, get_random_start, get_random_end
from src.maze_generation import write_maze_to_file


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.grid: CellGrid = self.init_grid()
        self.slider = Slider(
            (BOARD_SIZE - SLIDER_WIDTH) // 2,
            (BOARD_SIZE + SCREEN_HEIGHT - SLIDER_HEIGHT) // 2,
            SLIDER_WIDTH,
            SLIDER_HEIGHT,
        )
        self.logger = Logger()  # Khởi tạo Logger
        self.path = None  # Đường đi từ vị trí đầu đến cuối
        self.mouse_held = False
        self.heuristic = HeuristicType.MANHATTAN  # Loại hàm lượng giá mặc định

        self.step = 0  # Bước đi trong quá trình tìm đường
        self.mode = Mode.Cost  # Chế độ hiển thị mặc định
        self.autoAnimation = False

    def loop(self):
        
        evaluated_node = a_star_pure(self.grid, self.heuristic)
        print(f"Evaluated nodes: {evaluated_node}")
        
        path = backtrack_to_start(self.grid.get_end())
        
        if (WRITE_PATH):
            write_path_to_file(path, OUT_FILE_PATH)
        elif (WRITE_TEST):
            write_path_to_file(path, f"./testcase/output/output_{TESTCASE_NAME}.text")
            
        
        while True:
            
            self.handle_events()
            
            if (self.autoAnimation):
                if (self.step < self.max_steps):
                    self.step += 1  # tăng 1 bước
                else:
                    self.autoAnimation = False
                self.step += 1  # tăng 1 bước
                self.slider.set_value(self.step)  # Cập nhật thanh trượt
                time.sleep(0.1)
            
            self.max_steps = a_star(self.grid, self.step, self.logger, self.heuristic)
            # Tìm số bước đi đến đích
            self.step = min(
                self.step, self.max_steps
            )  # Đảm bảo bước hiện tại không vượt quá số bước đến đích

            self.slider.set_intervals(self.max_steps)
            self.slider.set_value(self.step)
            # Cập nhật thanh trượt dựa vào số bước đi hiện tại và số bước đi đến đích
            self.draw(self.screen)
            self.path = (
                backtrack_to_start(self.grid.get_end())
                if (self.max_steps == self.step)
                else None
            )
            pg.display.update()

    def handle_events(self):
        """
        Xử lý các sự kiện đầu vào từ người dùng như nhấn phím, nhấp chuột và kéo chuột.
        """
        for event in pg.event.get():    
            if event.type == pg.QUIT:
                quit(self)
            elif event.type == pg.KEYDOWN:
                handle_keydown(self, event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                start_drag(self)
            elif event.type == pg.MOUSEBUTTONUP:
                end_drag(self)
            elif event.type == pg.MOUSEMOTION and self.mouse_held:
                drag_toggle(self)

    def draw(self, surface: pg.Surface):
        """
        Vẽ lưới và các đường đi, cũng như hiển thị thanh trượt trên màn hình.
        """
        if self.grid is None:
            return
        draw_board(surface, self.grid, surface.get_rect(), self.mode)
        if self.slider is not None:
            self.slider.draw(surface)
        # Vẽ đường đi nếu có
        if self.path is not None:
            draw_path(surface, self.grid, self.path)

        # Vẽ thông tin logger
        self.logger.draw_log(surface)

    def init_grid(self):
        """
        Khởi tạo lưới cho trò chơi, tạo các ô trống và đặt ô bắt đầu và ô kết thúc.

        Parameters:
            width (int): Chiều rộng của lưới.
            height (int): Chiều cao của lưới.

        Returns:
            CellGrid: Đối tượng lưới chứa các ô và các cài đặt.
        """
        
        # Sinh bài toán một cách ngẫu nhiên
        if AUTO_MODE:
            # Sinh bản đồ một cách ngẫu nhiên
            grid = auto_gen_grid(GRID_SIZE)
            # Sinh ô bắt đầu và ô kết thúc
            start = get_random_start(grid)
            end = get_random_end(grid, start)
            
            if (WRITE_TEST):
                write_maze_to_file(grid, start, end, f"./testcase/input/input_{TESTCASE_NAME}.text")
                
            
            
            
        else:
            _, walls, start, end = read_input(INPUT_FILE_PATH)
            grid = gen_grid(GRID_SIZE, walls)


        print(f"Start: ({start[0]}, {start[1]})")
        print(f"End: ({end[0]}, {end[1]})")
        

        return CellGrid(self.screen.get_rect(), grid, start, end)

    def update_step(self, x):
        self.step = x

    def reset(self):
        """
        Tạo một lưới mới với các cài đặt ngẫu nhiên.
        """
        self.grid: CellGrid = self.init_grid(GRID_SIZE)
        self.slider = Slider(
            (BOARD_SIZE - SLIDER_WIDTH) // 2,
            (BOARD_SIZE + SCREEN_HEIGHT - SLIDER_HEIGHT) // 2,
            SLIDER_WIDTH,
            SLIDER_HEIGHT,
        )

        self.path = None  # Đường đi từ vị trí đầu đến cuối
        self.mouse_held = False
        self.step = 0  # Bước đi trong quá trình tìm đường
        self.mode = Mode.Cost  # Chế độ hiển thị mặc định
