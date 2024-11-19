def add_point(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> tuple[int, int]:
    """Adds two points represented as [x, y] coordinates."""
    return (pos_a[0] + pos_b[0], pos_a[1] + pos_b[1])


def print_queue(q):
    """Utility to print contents of a PriorityQueue without modifying it."""
    temp_queue = []
    while not q.empty():
        item = q.get()
        temp_queue.append(item)
        priority, cell = item
        print(f"Priority: {priority}, Position: {cell.pos}, Count: {cell.count}")

    for item in temp_queue:
        q.put(item)


def read_input(file_path: str):
    """
    Đọc file input từ đường dẫn `file_path`.
    
    File input được định dạng như sau:
    - Dòng 1: Kích thước bản đồ (n) - số nguyên.
    - Dòng 2: Danh sách vị trí các vật cản, định dạng: (x1,y1),(x2,y2),...
    - Dòng 3: Vị trí bắt đầu, định dạng: (x_start,y_start).
    - Dòng 4: Vị trí kết thúc, định dạng: (x_end,y_end).
    
    Returns:
        size (int): Kích thước bản đồ (n).
        walls (list[tuple[int, int]]): Danh sách các vị trí vật cản.
        start (tuple[int, int]): Vị trí ô bắt đầu.
        end (tuple[int, int]): Vị trí ô kết thúc.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Kiểm tra số dòng trong file
        if len(lines) < 4:
            raise ValueError("File input phải có ít nhất 4 dòng.")

        # Đọc kích thước bản đồ
        size = int(lines[0].strip())
        if size <= 0:
            raise ValueError("Kích thước bản đồ phải là số nguyên dương.")

        # Đọc vị trí các vật cản
        walls = [
            tuple(map(int, pos.strip("()").split(",")))
            for pos in lines[1].strip().split("),(")
        ]

        # Đọc vị trí ô bắt đầu và ô kết thúc
        start = tuple(map(int, lines[2].strip("()\n").split(",")))
        end = tuple(map(int, lines[3].strip("()\n").split(",")))

        return size, walls, start, end

    except FileNotFoundError:
        print(f"Error: File '{file_path}' không tồn tại.")
        raise
    except ValueError as e:
        print(f"Error: Lỗi định dạng file input - {e}")
        raise
    except Exception as e:
        print(f"Error: Đã xảy ra lỗi khi đọc file - {e}")
        raise



def read_map_size(file_path: str) -> int:
    """Đọc kích thước bản đồ từ file văn bản.
    """
    try:
        with open(file_path, 'r') as file:
            map_size = int(file.readline().strip())
        print(f"Map size: {map_size}")
        return map_size
    except Exception as e:
        print(f"Error reading map size: {e}")
        return -1  # Trả về 0 nếu xảy ra lỗi
    
    
def get_grid_size():
    """Đọc kích thước bản đồ từ người dùng nhập vào.
    """
    while True:
        try:
            # Yêu cầu người dùng nhập kích thước lưới
            size = int(input("Please enter map size (e.g., '5' for a 5x5 grid): ").strip())
            if size > 0:  # Kích thước lưới phải là số nguyên dương
                return size
            else:
                print("Map size must be a positive integer. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")



def write_testcase_to_file(map_size: int, walls: list[tuple[int, int]], start: tuple[int, int], end: tuple[int, int], file_path: str) -> None:
    try:
        # Mở file để ghi
        with open(file_path, 'w') as file:
            # Ghi map_size vào dòng đầu tiên
            file.write(f"{map_size}\n")
            
            # Ghi walls vào dòng thứ hai, chuyển đổi các tuple thành chuỗi
            walls_str = "),(".join([f"({x}, {y})" for x, y in walls])
            file.write(f"({walls_str})\n")
            
            # Ghi start vào dòng thứ ba
            file.write(f"({start[0]}, {start[1]})\n")
            
            # Ghi end vào dòng thứ tư
            file.write(f"({end[0]}, {end[1]})\n")
        
        # Thông báo thành công
        print("Test case written successfully.")
    
    except Exception as e:
        # Thông báo lỗi nếu có
        print(f"Failed to write test case to file. Error: {e}")
        



def write_path_to_file(path: list[tuple[int, int]], file_path: str) -> None:
    """Ghi danh sách các tọa độ đường đi vào file thành một dòng duy nhất.

    Parameters:
        path (list[tuple[int, int]]): Danh sách các tọa độ từ ô bắt đầu đến ô kết thúc.
        file_path (str): Đường dẫn tới file cần ghi kết quả.
    """
    try:
        with open(file_path, 'w') as file:
            # Chuyển các tọa độ thành chuỗi dạng "(x,y)" và nối với nhau bằng dấu phẩy
            path_str = ','.join([f"({pos[0]},{pos[1]})" for pos in path])
            # Ghi chuỗi vào file
            file.write(path_str)
        print(f"Path was written into {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        

