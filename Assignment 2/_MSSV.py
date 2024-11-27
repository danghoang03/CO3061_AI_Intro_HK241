import numpy as np
from state import *
import random
import time

agent_time = 0  # Tổng thời gian agent đã dùng (tính bằng giây)
MAX_AGENT_TIME = 120  # Thời gian tối đa cho cả ván đấu

# Kiểm tra điều kiện thắng trên bảng
def check_win(board):
    row_sum = np.sum(board, axis=1)
    col_sum = np.sum(board, axis=0)
    diag_sum1 = np.trace(board)
    diag_sum2 = np.trace(np.fliplr(board))

    if 3 in row_sum or 3 in col_sum or diag_sum1 == 3 or diag_sum2 == 3:
        return 1  # X thắng
    if -3 in row_sum or -3 in col_sum or diag_sum1 == -3 or diag_sum2 == -3:
        return -1  # O thắng
    return 0  # Không ai thắng


def evaluate_position(board, row, col, player):
    weights = [0.23, 0.2, 0.23, 0.2, 0.25, 0.2, 0.23, 0.2, 0.23]
    score = 0

    board[row, col] = player
    score += player * weights[3 * row + col]
    
    for i in range(3):
        row_sum = np.sum(board[i, :])
        col_sum = np.sum(board[:, i])
        diag_sum1 = np.trace(board)
        diag_sum2 = np.trace(np.fliplr(board))

        if row_sum == 2 * player or col_sum == 2 * player:  
            score += player

        if diag_sum1 ==  2 * player or diag_sum2 ==  2 * player:
            score += player
        
        if row_sum == 3 * player or col_sum == 3 * player:
            score += player * 5
        
        if diag_sum1 == 3 * player or diag_sum2 == 3 * player:
            score += player * 5
    score += check_win(board) * 15
    
    board[row, col] = -player
    
    for i in range(3):
        row_sum = np.sum(board[i, :])
        col_sum = np.sum(board[:, i])
        diag_sum1 = np.trace(board)
        diag_sum2 = np.trace(np.fliplr(board))
        
        if row_sum == -3 * player or col_sum == -3 * player:
            score += player * 2
        
        if diag_sum1 == -3 * player or diag_sum2 == -3 * player:
            score += player * 2

    board[row, col] = 0
    return score


# Hàm đánh giá bảng cục bộ
def evaluate_local_board(board):
    weights = [0.23, 0.2, 0.23, 0.2, 0.25, 0.2, 0.23, 0.2, 0.23]
    score = 0

    for cell in range(9):
        score += board[cell // 3, cell % 3] * weights[cell]
    
    # Kiểm tra các hàng, cột, và đường chéo
    for i in range(3):
        row_sum = np.sum(board[i, :])
        col_sum = np.sum(board[:, i])

        if row_sum == 2 or col_sum == 2:  # Người chơi gần thắng
            score += 6
        elif row_sum == -2 or col_sum == -2:  # Đối thủ gần thắng
            score -= 6

        # Đường chéo
        diag_sum1 = np.trace(board)
        diag_sum2 = np.trace(np.fliplr(board))

        if diag_sum1 == 2 or diag_sum2 == 2:
            score += 7
        elif diag_sum1 == -2 or diag_sum2 == -2:
            score -= 7
            
    if (board[0, 0] + board[0, 1] == -2 and board[0, 2] == 1) or (
            board[0, 1] + board[0, 2] == -2 and board[0, 0] == 1) or (
            board[0, 0] + board[0, 2] == -2 and board[0, 1] == 1):
        score += 9

    if (board[1, 0] + board[1, 1] == -2 and board[1, 2] == 1) or (
            board[1, 1] + board[1, 2] == -2 and board[1, 0] == 1) or (
            board[1, 0] + board[1, 2] == -2 and board[1, 1] == 1):
        score += 9

    if (board[2, 0] + board[2, 1] == -2 and board[2, 2] == 1) or (
            board[2, 1] + board[2, 2] == -2 and board[2, 0] == 1) or (
            board[2, 0] + board[2, 2] == -2 and board[2, 1] == 1):
        score += 9

    if (board[0, 0] + board[1, 0] == -2 and board[2, 0] == 1) or (
            board[1, 0] + board[2, 0] == -2 and board[0, 0] == 1) or (
            board[0, 0] + board[2, 0] == -2 and board[1, 0] == 1):
        score += 9

    if (board[0, 1] + board[1, 1] == -2 and board[2, 1] == 1) or (
            board[1, 1] + board[2, 1] == -2 and board[0, 1] == 1) or (
            board[0, 1] + board[2, 1] == -2 and board[1, 1] == 1):
        score += 9

    if (board[0, 2] + board[1, 2] == -2 and board[2, 2] == 1) or (
            board[1, 2] + board[2, 2] == -2 and board[0, 2] == 1) or (
            board[0, 2] + board[2, 2] == -2 and board[1, 2] == 1):
        score += 9

    if (board[0, 0] + board[1, 1] == -2 and board[2, 2] == 1) or (
            board[1, 1] + board[2, 2] == -2 and board[0, 0] == 1) or (
            board[0, 0] + board[2, 2] == -2 and board[1, 1] == 1):
        score += 9

    if (board[0, 2] + board[1, 1] == -2 and board[2, 0] == 1) or (
            board[1, 1] + board[2, 0] == -2 and board[0, 2] == 1) or (
            board[0, 2] + board[2, 0] == -2 and board[1, 1] == 1):
        score += 9

    if (board[0, 0] + board[0, 1] == 2 and board[0, 2] == -1) or (
            board[0, 1] + board[0, 2] == 2 and board[0, 0] == -1) or (
            board[0, 0] + board[0, 2] == 2 and board[0, 1] == -1):
        score -= 9

    if (board[1, 0] + board[1, 1] == 2 and board[1, 2] == -1) or (
            board[1, 1] + board[1, 2] == 2 and board[1, 0] == -1) or (
            board[1, 0] + board[1, 2] == 2 and board[1, 1] == -1):
        score -= 9

    if (board[2, 0] + board[2, 1] == 2 and board[2, 2] == -1) or (
            board[2, 1] + board[2, 2] == 2 and board[2, 0] == -1) or (
            board[2, 0] + board[2, 2] == 2 and board[2, 1] == -1):
        score -= 9

    if (board[0, 0] + board[1, 0] == 2 and board[2, 0] == -1) or (
            board[1, 0] + board[2, 0] == 2 and board[0, 0] == -1) or (
            board[0, 0] + board[2, 0] == 2 and board[1, 0] == -1):
        score -= 9

    if (board[0, 1] + board[1, 1] == 2 and board[2, 1] == -1) or (
            board[1, 1] + board[2, 1] == 2 and board[0, 1] == -1) or (
            board[0, 1] + board[2, 1] == 2 and board[1, 1] == -1):
        score -= 9

    if (board[0, 2] + board[1, 2] == 2 and board[2, 2] == -1) or (
            board[1, 2] + board[2, 2] == 2 and board[0, 2] == -1) or (
            board[0, 2] + board[2, 2] == 2 and board[1, 2] == -1):
        score -= 9

    if (board[0, 0] + board[1, 1] == 2 and board[2, 2] == -1) or (
            board[1, 1] + board[2, 2] == 2 and board[0, 0] == -1) or (
            board[0, 0] + board[2, 2] == 2 and board[1, 1] == -1):
        score -= 9

    if (board[0, 2] + board[1, 1] == 2 and board[2, 0] == -1) or (
            board[1, 1] + board[2, 0] == 2 and board[0, 2] == -1) or (
            board[0, 2] + board[2, 0] == 2 and board[1, 1] == -1):
        score -= 9
    
    score += check_win(board) * 12
    return score


def evaluation_state(state):
    weights = [1.4, 1, 1.4, 1, 1.75, 1, 1.4, 1, 1.4]
    score = 0
    
    for i in range(9):
        block_score = evaluate_local_board(state.blocks[i])
        score += 1.5 * block_score * weights[i]
        score += state.global_cells[i] * weights[i]

    global_score = evaluate_local_board(state.global_cells.reshape(3, 3))
    score += global_score * 150
    win = check_win(state.global_cells.reshape(3, 3))
    if win != 0:
        score += win * 5000  # Ưu tiên thắng trò chơi

    return score

def order_moves(state, valid_moves):
    move_scores = []
    for move in valid_moves:
        local_board = state.blocks[move.index_local_board]
        move_score = evaluate_position(local_board, move.x, move.y, move.value)
        move_scores.append((move, move_score))

    # Nếu là lượt của X (1), ưu tiên bước đi với điểm cao nhất; nếu là O (-1), ưu tiên điểm thấp nhất.
    if state.player_to_move == state.X:
        move_scores.sort(key=lambda x: -x[1])  # Giảm dần
    else:
        move_scores.sort(key=lambda x: x[1])  # Tăng dần

    # Trả về danh sách bước đi đã sắp xếp
    return [move for move, score in move_scores]



def minimax(state, depth, alpha, beta, start_time):
    if state.game_over or depth == 0 or time.time() - start_time > 9:
        return evaluation_state(state)

    valid_moves = state.get_valid_moves
    ordered_moves = order_moves(state, valid_moves)
     
    if state.player_to_move == state.X:
        max_utility = -float('inf')
        for move in ordered_moves:
            if time.time() - start_time > 9:
                break
            child_state = State(state)
            child_state.free_move = state.free_move
            child_state.act_move(move)
            utility = minimax(child_state, depth - 1, alpha, beta, start_time)
            if utility > max_utility:
                max_utility = utility
            if max_utility > alpha:
                alpha = max_utility
            if alpha >= beta:
                break
        return alpha
    else:
        min_utility = float('inf')
        for move in ordered_moves:
            if time.time() - start_time > 9:
                break
            child_state = State(state)
            child_state.free_move = state.free_move
            child_state.act_move(move)
            utility = minimax(child_state, depth - 1, alpha, beta, start_time)
            if utility < min_utility:
                min_utility = utility
            if min_utility < beta:
                beta = min_utility
            if beta <= alpha:
                break
        return beta


numMoves = 0


def select_move(cur_state, remain_time):
    global agent_time
    start_time = time.time()
    
    valid_moves = cur_state.get_valid_moves
    if len(valid_moves) == 0:
        return None

    for move in valid_moves:
        child_state = State(cur_state)
        child_state.free_move = cur_state.free_move
        child_state.act_move(move)
        if child_state.game_over is True:
            return move

    global numMoves

    if numMoves == 0 and cur_state.player_to_move == cur_state.X:
        numMoves += 1
        agent_time += time.time() - start_time
        return UltimateTTT_Move(4, 1, 1, cur_state.X)
    
    ordered_moves = order_moves(cur_state, valid_moves)
    scores = np.zeros(len(valid_moves))
    
    time_left = MAX_AGENT_TIME - agent_time
    if time_left < 10:  
        depth = 2
    elif time_left < 30:
        depth = 3
    elif numMoves < 14: 
        if cur_state.free_move is True:
            depth = 2
        else:
            depth = 3
    elif numMoves < 20:
        if cur_state.free_move is True:
            depth = 3
        else:
            depth = 4
    else:
        if cur_state.free_move is True:
            depth = 4
        else:
            depth = 5
    
    for i, move in enumerate(ordered_moves):
        scores[i] += evaluate_position(cur_state.blocks[move.index_local_board], move.x, move.y, move.value) * 45

    for i, move in enumerate(ordered_moves):
        time_spent = time.time() - start_time
        if time_spent > 9:
            break
        child_state = None
        if type(cur_state) is State:
            child_state = State(cur_state)
        else:
            child_state = State_2(cur_state)
        child_state.free_move = cur_state.free_move
        child_state.act_move(move)

        alpha = -float('inf')
        beta = float('inf')
        utility = minimax(child_state, depth, alpha, beta, start_time)

        scores[i] += utility
    
    best_move = None
    if valid_moves[0].value == 1:
        best_score = -float('inf')
        for i, move in enumerate(ordered_moves):
            if scores[i] > best_score:
                best_score = scores[i]
                best_move = [move]
            elif scores[i] == best_score:
                best_move.append(move)
    else:
        best_score = float('inf')
        for i, move in enumerate(ordered_moves):
            if scores[i] < best_score:
                best_score = scores[i]
                best_move = [move]
            elif scores[i] == best_score:
                best_move.append(move)

    numMoves += 1
    return random.choice(best_move)
