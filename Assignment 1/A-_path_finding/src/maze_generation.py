import random
from typing import List, Tuple

from src.grid import Cell
from src.types import CellType, CellMark


# Hàm tạo lưới mê cung ban đầu
def create_grid(rows: int, cols: int) -> List[List[Cell]]:
    grid = [[Cell(type=CellType.Empty, pos=(i, j)) for j in range(cols)] for i in range(rows)]
    return grid


# Hàm khởi tạo điểm bắt đầu và kết thúc
def initialize_start_end(grid: List[List[Cell]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    start = (0, random.randint(1, rows - 2))
    end = (cols - 1, random.randint(1, rows - 2))

    grid[start[0]][start[1]].mark = CellMark.Start
    grid[start[0]][start[1]].type = CellType.Empty
    grid[end[0]][end[1]].mark = CellMark.End
    grid[end[0]][end[1]].type = CellType.Empty

    return start, end


# Hàm khởi tạo trạng thái ngẫu nhiên trong mê cung
def initialize_random(grid: List[List[Cell]]):
    rows, cols = len(grid), len(grid[0])
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if random.random() < 0.5:  # Xác suất tạo tường
                grid[i][j].type = CellType.Wall


# Hàm đếm số hàng xóm "trống" xung quanh một ô
def count_neighbors(grid: List[List[Cell]], x: int, y: int) -> int:
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny].type == CellType.Empty:
            count += 1
    return count


# Hàm cập nhật mê cung theo Cellular Automaton
def update_grid(grid: List[List[Cell]], birth: List[int], survival: List[int]):
    rows, cols = len(grid), len(grid[0])
    new_grid = [[cell for cell in row] for row in grid]  # Tạo bản sao lưới

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if grid[i][j].mark in (CellMark.Start, CellMark.End):
                continue  # Bỏ qua các ô đặc biệt
            neighbors = count_neighbors(grid, i, j)
            if grid[i][j].type == CellType.Wall and neighbors in birth:
                new_grid[i][j].type = CellType.Empty
            elif grid[i][j].type == CellType.Empty and neighbors not in survival:
                new_grid[i][j].type = CellType.Wall

    return new_grid



# Hàm kiểm tra tính khả thi của mê cung (từ điểm bắt đầu đến kết thúc)
def is_solvable(grid: List[List[Cell]], start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    rows, cols = len(grid), len(grid[0])
    visited = set()
    stack = [start]

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            return True
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny].type == CellType.Empty and (nx, ny) not in visited:
                stack.append((nx, ny))

    return False


# Hàm chính để tạo mê cung
def generate_maze(rows: int, cols: int, birth: List[int], survival: List[int]):
    grid = create_grid(rows, cols)
    start, end = initialize_start_end(grid)
    initialize_random(grid)

    iterations = 0
    while iterations < 300:
        grid = update_grid(grid, birth, survival)
        iterations += 1
        if is_solvable(grid, start, end):
            print(f"Mê cung được tạo sau {iterations} lần lặp.")
            return grid, start, end

    print("Không thể tạo mê cung khả thi sau 300 lần lặp.")
    return None, None, None


def write_maze_to_file(grid: List[List[Cell]], start: tuple[int, int], end: tuple[int, int], file_path: str) -> None:
    """Luu lai ban do duoc tao vao file input.text
    
    format:
    n -> kich thuoc ban do n * n
    (x,y),(m,n),(k,l),... -> danh sach cac diem vat can
    (xstart,ystart)
    (xend,yend)
    """
    
    try:
        with open(file_path, 'w') as file:
            size = max(len(grid[0]), len(grid))
            file.write(f"{size}\n")
            
            wall_list = ''
            
            for cells in grid:
                for cell in cells:
                    if cell.type == CellType.Wall:
                        wall_list += f"({cell.pos[0]},{cell.pos[1]}),"
             
            if len(wall_list) > 0:            
                wall_list = wall_list.rstrip(',') + "\n"
            file.write(wall_list)
            
            file.write(f"({start[0]},{start[1]})\n")
            file.write(f"({end[0]},{end[1]})\n")
            
        print(f"Write map successfully into {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")