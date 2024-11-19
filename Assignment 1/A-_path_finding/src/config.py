TEST_NAMES = [
    '',  # File 10 * 10
    '1', # File 20 * 20
    '2', # File 100 * 100  
    '3',  # File 2000 * 2000
    # 'test1'
]

# Chọn file bạn muốn sử dụng (chỉ số 0, 1, 2, hoặc 3 để chọn file tương ứng)
index = 2

# Ghép chuỗi để tạo đường dẫn file tương ứng với index
INPUT_FILE_PATH = f"./testcase/input/input{TEST_NAMES[index]}.text"
OUT_FILE_PATH = f"./testcase/output/output{TEST_NAMES[index]}.text"

# Ex: index = 2 -> 
# ./testcase/input/input2.text
# ./testcase/output/output2.text

# In ra thông tin đã chọn
print(f"Using input file: {INPUT_FILE_PATH}")
print(f"Using output file: {OUT_FILE_PATH}")




from src.types import HeuristicType
from src.utils import read_map_size, get_grid_size


# Tùy chỉnh các thông số cố định UI
GAME_TITLE = "A* Pathfinding"  # Tên cửa sổ

AUTO_MODE = (
    input(
        "Choose Auto mode? (y/n)\n(y means randomize map, other key means read from input file): "
    ).lower()
    == "y"
)  # Chế độ tự động

if AUTO_MODE:
    print("Auto mode activated.")
else:
    print(f"Manual mode activated.\nMap will be read from {INPUT_FILE_PATH}")
  
TESTCASE_NAME = ''
WRITE_TEST = False
WRITE_PATH = False

if AUTO_MODE:
    WRITE_TEST = (
        input(
            "Do you want write testcase generated and path into file (y/n)\n(y means write into file, other key means do not write): "
        ).lower()
        == "y"
    )


if (not AUTO_MODE):  
    WRITE_PATH = (
        input(
            "Do you want write path found into file (y/n)\n(y means write into file, other key means do not write): "
        ).lower()
        == "y"
    )

elif (AUTO_MODE and WRITE_TEST):
    TESTCASE_NAME = (
        input("Please enter the file name: ").strip().lower()
    )



SCREEN_WIDTH = 1000  # Chiều rộng cửa sổ
SCREEN_HEIGHT = 800  # Chiều cao cửa sổ
MARGIN = 5  # Lề


BOARD_SIZE = 700  # Kích thước bảng === chiều rộng cửa sổ


if AUTO_MODE:
    GRID_SIZE = get_grid_size()
else:
    GRID_SIZE = read_map_size(INPUT_FILE_PATH)



CELL_COLOR_EMPTY = (60, 60, 60)  # Màu ô trống
CELL_COLOR_WALL = (139, 69, 19)  # Màu của ô vật cản
CELL_GAP = 1  # Khoảng cách giữa các ô
CELL_CURRENT_COLOR = (0, 255, 255)
CELL_NEXT_COLOR = (255, 0, 0)
CELL_SIZE = (
    BOARD_SIZE - 2 * MARGIN - ((GRID_SIZE - 1) * CELL_GAP)
) / GRID_SIZE  # Kích thước hình vuông của mỗi ô
PATH_LINE_WIDTH = 3  # Độ dày của đường đi

FONT_SIZE = round(CELL_SIZE) // 2  # Cỡ chữ
LOGGER_FONT_SIZE = 25  # Cỡ chữ logger
FONT_COLOR = (255, 255, 255)  # Màu chữ

SLIDER_WIDTH = BOARD_SIZE // 2  # Chiều rộng thanh trượt
SLIDER_HEIGHT = 20  # Chiều cao thanh trượt
SLIDER_BAR_COLOR = (100, 100, 100)  # Màu của thanh trượt
SLIDER_THUMB_SIZE = SLIDER_HEIGHT * 1.5  # Kích thước nút trượt
SLIDER_THUMB_COLOR = (255, 255, 255)  # Màu của nút trượt

ARROW_COLOR = (255, 255, 255)  # Màu mũi tên
ARROW_SIZE = 2  # Độ dày mũi tên
