import numpy as np
import pygame
from state import *

def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    if len(valid_moves) != 0:
        return np.random.choice(valid_moves)
    return None

# # Người chơi tự điều khiển
# def select_move(cur_state, remain_time):
#     # Lấy danh sách các nước đi hợp lệ
#     valid_moves = cur_state.get_valid_moves
    
#     # Nếu có nước đi hợp lệ
#     if len(valid_moves) != 0:
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.MOUSEBUTTONDOWN:  # Khi người chơi nhấn chuột
#                     mouse_x, mouse_y = pygame.mouse.get_pos()
                    
#                     # Tính toán block được chọn
#                     block_x = mouse_x // 200
#                     block_y = mouse_y // 200
#                     index_local_board = block_y * 3 + block_x

#                     # Tính toán tọa độ x, y trong block (ĐÃ ĐIỀU CHỈNH PADDING)
#                     x = (mouse_y % 200 - 35) // 50
#                     y = (mouse_x % 200 - 35) // 50
                    
#                     # Xác định ô trong bảng cục bộ từ chỉ số hàng và cột
#                     selected_move = None
#                     for move in valid_moves:
#                         if move.x == x and move.y == y and move.index_local_board == index_local_board:
#                             selected_move = move
#                             break
                    
#                     # Nếu nước đi hợp lệ
#                     if selected_move is not None:
#                         return selected_move
#                     else:
#                         print("Invalid move. Try again.")
#     return None