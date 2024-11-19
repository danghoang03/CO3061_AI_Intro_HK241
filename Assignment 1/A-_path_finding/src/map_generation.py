import random
from src.grid import Cell
from src.types import CellType, CellMark
from src.maze_generation import generate_maze


def auto_gen_grid(
    map_size: int
) -> list[list[Cell]]:

    grid, start, end = generate_maze(map_size, map_size, [2], [2,3])
    
    # remove start and end created by generate_maze function
    grid[start[0]][start[1]].mark = CellMark.No
    grid[end[0]][end[1]].mark = CellMark.No
    
    return grid

def gen_grid(
    map_size: int, walls: list[tuple[int, int]] = None
) -> list[list[Cell]]:
    """Sinh bản đồ cùng với các vật cản

    Args:
        map_size int: Kích thước bản đồ map(map_size * map_size)
        walls ([List[Tuple[int, int]]]): Danh sách các ô vật cản

    Returns:
        List[List[Cell]]: Mảng 2 chiều chứa các ô kiểu Cell
    """

    grid = [
        [Cell(type=CellType.Empty, pos=(x, y)) for y in range(map_size)]
        for x in range(map_size)
    ]

    # Place walls based on the provided wall list
    for x, y in walls:
        if 0 <= x < map_size and 0 <= y < map_size:  # Ensure the wall is within bounds
            grid[x][y].type = CellType.Wall
    return grid



# Sinh trạng thái mở đầu
def get_random_start(grid: list[list[Cell]]) -> tuple[int, int]:
    """Chọn một điểm ngẫu nhiên không phải là CellType.Wall từ lưới.

    Args:
        grid (list[list[Cell]]): Lưới các ô (Cell) với các vật cản và ô trống.

    Returns:
        tuple[int, int]: Tọa độ (x, y) của điểm không phải là CellType.Wall.
        
    Error:
        Game có thể treo nếu không có bất kỳ vị trí trống nào để chọn làm trạng thái bắt đầu.
    """
    width = len(grid)
    height = len(grid[0])

    while True:
        # Chọn một tọa độ ngẫu nhiên (x, y)
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # Kiểm tra nếu ô không phải là CellType.Wall
        if grid[x][y].type != CellType.Wall:
            return (x, y)


# Sinh trạng thái kết thúc
def get_random_end(grid: list[list[Cell]], start: tuple[int, int]) -> tuple[int, int]:
    """Chọn một điểm ngẫu nhiên không phải là CellType.Wall và không trùng với điểm bắt đầu.

    Args:
        grid (list[list[Cell]]): Lưới các ô (Cell) với các vật cản và ô trống.
        start (tuple[int, int]): Tọa độ của điểm bắt đầu.

    Returns:
        tuple[int, int]: Tọa độ (x, y) của điểm kết thúc không phải là CellType.Wall và không trùng với điểm bắt đầu.
        
    Error:
        Game có thể treo nếu không có bất kỳ vị trí trống nào để chọn làm trạng thái bắt đầu.
    """
    width = len(grid)
    height = len(grid[0])

    while True:
        # Chọn một tọa độ ngẫu nhiên (x, y)
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # Kiểm tra nếu ô không phải là CellType.Wall và không trùng với điểm bắt đầu
        if grid[x][y].type != CellType.Wall and (x, y) != start:
            return (x, y)
