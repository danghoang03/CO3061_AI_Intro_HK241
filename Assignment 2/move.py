import numpy as np
from state import State_2, UltimateTTT_Move
from keras.models import load_model

# Tải mô hình đã huấn luyện
model = load_model('tictactoe_model_epoch_9_20241228191727.h5')

def board_to_array(state):
    board = state.blocks
    array = np.zeros((9, 9))
    for i in range(9):
        for x in range(3):
            for y in range(3):
                array[i // 3 * 3 + x, i % 3 * 3 + y] = board[i][x, y]
    return array

def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    if not valid_moves:
        return None

    best_move = None
    best_value = -float('inf')

    for move in valid_moves:
        # Tạo bản sao của trạng thái hiện tại
        state_copy = State_2(cur_state)
        state_copy.free_move = cur_state.free_move
        state_copy.act_move(move)
        board_array = board_to_array(state_copy)
        board_array = board_array.reshape(1, 9, 9)
        policy, value = model.predict(board_array)
        cur_value = value[0][0]

        if cur_value > best_value:
            best_value = cur_value
            best_move = move

    return best_move