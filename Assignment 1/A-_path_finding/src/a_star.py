import math
from queue import PriorityQueue

from src.grid import Cell, CellGrid
from src.types import HeuristicType
from src.ui import Logger




def a_star(
    grid: CellGrid, step: int, logger: Logger, heuristic_type: HeuristicType
) -> int:
    """
    Hàm thực hiện thuật toán A*.
    Hàm sẽ thực hiện việc tìm kiếm và trả về số bước tối đa bằng cách sử dụng trọng số ẩn của mỗi ô,
    trọng số ẩn (hidden) sẽ tương tự như trọng số thật (count) nhưng không hiển thị trên lưới.
    Mục đích là để tìm số bước tối đa nhưng vẫn hiển thị theo số bước hiện tại

    Parameters:
        grid (CellGrid): Lưới chứa các ô và thông tin vị trí bắt đầu và kết thúc.
        step (int): Số bước hiện tại trong thuật toán A*, dùng để hỗ trợ việc thay đổi bước trên UI, slider.

    Returns:
        int: Tổng số bước tối đa để thực hiện quá trình tìm kiếm.
    """
    
    grid.clear_count()  # Xóa thông tin cũ
    start, end = grid.get_start(), grid.get_end()  # Vị trí bắt đầu và vị trí kết thúc
    start.hidden = 0  # Trọng ẩn của mỗi ô, tương dương với count nhưng ẩn
    start.update_cell(
        0, None, heuristic(end.pos, start.pos, heuristic_type)
    )  # Update giá trị của ô bắt đầu
    max_steps = 0  # Biến đêm số bước tối đa

    initial_step = step

    frontier = PriorityQueue()  # Hàng đợi ưu tiên
    frontier.put((0, start))  # Thêm vị trí bắt đầu vào hàng đợi
    visited = set()  # Các ô đã duyệt
    visited.add(start.pos)  # Thêm vị trí bắt đầu vào Set đã duyệt
    while not frontier.empty():  # Duyệt đến khi hàng đợi rỗng
        _, current = frontier.get()
        # Lấy ô đầu tiên từ hàng đợi, tức ô có độ ưu tiên thấp nhất,
        # độ ưu tiên được tính bằng hàm tổng của Số bước từ ô bắt đầu + hàm lượng giá từ ô hiện tại đến ô kết thúc

        if current.pos == end.pos:  # Nếu ô hiện tại là ô kết thúc thì dừng
            break

        for next in grid.get_neighbors(current.pos):
            # Duyệt qua các ô lân cận của ô hiện tại
            # Lưu ý: thứ tự duyệt của ô lân cận không cố định mà sẽ thay đổi
            # tùy thuộc vào vị trí của ô hiện tại
            # Ô hiện tại có tổng hoành độ và tung độ là số Chẵn thì sẽ duyệt theo thứ tự: trên, trái, dưới, phải
            #                                              Lẻ                           : phải, dưới, trái, trên
            # Điều này giúp ưu tiên tìm theo đường chéo thay vì theo hàng ngang hoặc hàng dọc
            new_cost = current.hidden + 1
            if next.pos not in visited or new_cost < next.hidden:
                visited.add(next.pos)
                heuristic_value = heuristic(end.pos, next.pos, heuristic_type)
                priority = new_cost + heuristic_value
                # Nếu ô lân cận chưa được duyệt hoặc có trọng số mới nhỏ hơn trọng số cũ
                # thì cập nhật trọng số mới và thêm vào hàng đợi ưu tiên với độ ưu tiên dựa vào
                # số bước từ ô bắt đầu + hàm lượng giá từ ô hiện tại đến ô kết thúc
                next.hidden = new_cost
                frontier.put((priority, next))
                if step > 0:
                    next.update_cell(new_cost, current, heuristic_value)
                    # Cập nhật thông tin của ô lân cận bao gồm số bước, trọng số, tọa độ ô hiện tại (để truy vết)
                    # để hiển thị trên lưới nếu số bước (step) còn lớn hơn 0
        if step == 1:
            current.is_current = True  # Đánh dấu ô hiện tại là ô đang được xét
            list(frontier.queue)[0][
                1
            ].is_next = True  # Đánh dấu ô đầu tiên trong queue là ô được xét tiếp theo
            logger.update(
                list(frontier.queue), current, initial_step, heuristic_type
            )  # Cập nhật thông tin cho logger

        max_steps += 1
        step -= 1

    return max_steps


def backtrack_to_start(end: Cell) -> list[tuple[int, int]]:
    """
    Truy vết lại đường đi từ ô đích đến ô bắt đầu dựa trên thông tin ô trước đó trong `path_from`.

    Parameters:
        end (Cell): Ô kết thúc.

    Returns:
        list[tuple[int, int]]: Danh sách các tọa độ từ ô bắt đầu đến ô kết thúc.
    """

    current = end
    path = []

    while current is not None:
        path.append(current.pos)
        current = current.path_from

    path.reverse()  # Đảo ngược danh sách để có thứ tự từ ô bắt đầu đến ô kết thúc
    return path


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    # Hàm tính khoảng cách Manhattan giữa 2 điểm
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_distance(a: tuple[int, int], b: tuple[int, int]) -> float:
    # Hàm tính khoảng cách Euclidean giữa 2 điểm
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def heuristic(
    goal: tuple[int, int], next: tuple[int, int], heuristic: HeuristicType
) -> float:
    """Estimate the distance from the next point to the goal using the selected heuristic."""
    if heuristic == HeuristicType.MANHATTAN:
        return manhattan_distance(goal, next)
    elif heuristic == HeuristicType.EUCLIDEAN:
        return euclidean_distance(goal, next)
    elif heuristic == HeuristicType.COMBINED:
        return manhattan_distance(goal, next) + euclidean_distance(goal, next)
    else:
        raise ValueError("Invalid heuristic type selected.")


# pure a* function, not contain ui code
def a_star_pure(grid: CellGrid, heuristic_type: HeuristicType) -> int:
    start, end = grid.get_start(), grid.get_end()
    start.hidden = 0
    start.update_cell(0, None, heuristic(end.pos, start.pos, heuristic_type))
    max_steps = 0

    frontier = PriorityQueue()
    frontier.put((0, start))
    visited = set()
    visited.add(start.pos)
    while not frontier.empty():
        _, current = frontier.get()

        if current.pos == end.pos:
            break

        for next in grid.get_neighbors(current.pos):
            new_cost = current.hidden + 1
            if next.pos not in visited or new_cost < next.hidden:
                visited.add(next.pos)
                heuristic_value = heuristic(end.pos, next.pos, heuristic_type)
                priority = new_cost + heuristic_value
                next.hidden = new_cost
                frontier.put((priority, next))
                next.update_cell(new_cost, current, heuristic_value)
        max_steps += 1

    return max_steps