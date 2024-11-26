import logging
from typing import Literal
import numpy as np
from state import State, UltimateTTT_Move
import copy


def select_move(cur_state: State, remain_time: float | Literal[120]):
    valid_moves = cur_state.get_valid_moves
    count_O = len(np.where(cur_state.blocks == cur_state.O)[0])
    if count_O < 5:
        return np.random.choice(valid_moves)

    utility, action = minimax(
        cur_state, cur_state.player_to_move, 5, -float("inf"), +float("inf")
    )
    if action:
        return action
    else:
        if len(valid_moves) != 0:
            return np.random.choice(valid_moves)


def reduce_moves(cur_state: State, moves: list[UltimateTTT_Move]):
    winable_block_indices = []
    opponent_winning_blocks = []

    for i in range(9):
        block = cur_state.blocks[i]

        if cur_state.global_cells[i] == 0:
            if count_positions_can_win(block, cur_state.player_to_move) >= 1:
                winable_block_indices.append(i)
            elif count_positions_can_win(block, -cur_state.player_to_move) >= 1:
                opponent_winning_blocks.append(i)

    if len(winable_block_indices) > 0:
        filter_func = lambda move: move.index_local_board in winable_block_indices
        return list(filter(filter_func, moves))

    if len(opponent_winning_blocks) > 0:
        filter_func = lambda move: move.index_local_board in opponent_winning_blocks
        return list(filter(filter_func, moves))

    random_local_index = np.random.choice(np.array(range(9)))
    filter_func = lambda move: move.index_local_board == random_local_index
    return list(filter(filter_func, moves))


def minimax(
    gameState: State, player: int, depth: int, alpha: float, beta: float
) -> tuple[int, UltimateTTT_Move]:
    if gameState.game_over or depth == 0:
        return (evaluate(gameState), UltimateTTT_Move(-1, -1, -1, 0))

    moves = gameState.get_valid_moves
    if gameState.free_move:
        moves = reduce_moves(gameState, moves)

    # For maximize plyer
    if player == 1:
        value = float("-inf")
        best_move = None
        for action in moves:
            new_state = copy.deepcopy(gameState)
            new_state.act_move(action)
            score, _ = minimax(new_state, -player, depth - 1, alpha, beta)
            if score > value:
                value = score
                best_move = action
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return value, best_move

    else:
        value = float("inf")
        best_move = None
        for action in moves:
            new_state = copy.deepcopy(gameState)
            new_state.act_move(action)
            score, _ = minimax(new_state, -player, depth - 1, alpha, beta)
            if score < value:
                value = score
                best_move = action
            beta = min(beta, score)
            if beta <= alpha:
                break
        return value, best_move


def evaluate(cur_state: State) -> int:
    game_result = cur_state.game_result(np.reshape(cur_state.global_cells, (3, 3)))

    score = 0
    previous_move = cur_state.previous_move
    cur_block = cur_state.blocks[previous_move.index_local_board]
    cur_player = cur_state.previous_move.value
    if game_result is None:
        game_result = 0
    elif game_result != 0:
        return float("inf") * game_result

    cur_block_result = cur_state.game_result(cur_block)
    if cur_block_result is not None:
        score += 100 * cur_block_result
        local_board_pos = (
            previous_move.index_local_board // 3,
            previous_move.index_local_board % 3,
        )
        score += cur_block_result * evaluate_local_board(
            np.reshape(cur_state.global_cells, (3, 3)),
            cur_player,
            UltimateTTT_Move(-1, local_board_pos[0], local_board_pos[1], cur_player),
        )

    else:
        score += cur_player * evaluate_local_board(cur_block, cur_player, previous_move)

    return score + np.sum(cur_state.global_cells) * 100


def count_player_in_block(cur_block: np.ndarray, player: int) -> int:
    return np.count_nonzero(cur_block == player)


def evaluate_local_board(
    block: np.ndarray, player: int, previous_move: UltimateTTT_Move
) -> int:
    opponent = -player
    # Get the number of positions where the player and opponent can win
    count_opponent_wins_pos = count_positions_can_win(block, opponent)
    count_player_wins_pos = count_positions_can_win(block, player)

    score = 0

    # Count the player's and opponent's marks on the block
    count_opponent_pos = count_player_in_block(block, opponent)
    count_player_pos = count_player_in_block(block, player)

    # Priority check if opponent has no marks (0 positions occupied)
    if count_opponent_pos == 0:
        if count_player_pos == 1:  # First move by player, prioritizing corners
            score += (
                2
                if (previous_move.x, previous_move.y)
                in [(0, 0), (0, 2), (2, 0), (2, 2)]
                else 0
            )
        elif count_player_pos == 2:  # Second move, prioritizing center
            score += 2 if (previous_move.x, previous_move.y) == (1, 1) else 0

    else:  # Case where both player and opponent have positions in the block
        if count_player_pos == 1 and count_opponent_pos == 1:  # Both have one mark
            position = np.where(block == opponent)
            if (position[0][0], position[1][0]) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                score += 3 if (previous_move.x, previous_move.y) == (1, 1) else 0
            else:
                score += (
                    2
                    if (previous_move.x, previous_move.y)
                    in [(0, 0), (0, 2), (2, 0), (2, 2)]
                    else 0
                )
        else:
            # Player makes a move in the center or corner
            score += 1 if (previous_move.x, previous_move.y) == (1, 1) else 0
            score += (
                1
                if (previous_move.x, previous_move.y)
                in [(0, 0), (0, 2), (2, 0), (2, 2)]
                else 0
            )

    if count_opponent_wins_pos >= 2:
        score -= 11

    elif count_opponent_wins_pos >= 1:
        score -= 6

    if count_player_wins_pos >= 2:
        score += 10

    elif count_player_wins_pos >= 1:
        score += 5

    return score


def count_positions_can_win(cur_block: np.ndarray, player_maker: int) -> int:
    total_wins = 0

    # Row and Column Checks
    for i in range(3):
        # Row win check: 2 of the same player and 1 empty space
        if (
            np.count_nonzero(cur_block[i] == player_maker) == 2
            and np.count_nonzero(cur_block[i] == 0) == 1
        ):
            total_wins += 1

        # Column win check: 2 of the same player and 1 empty space
        if (
            np.count_nonzero(cur_block[:, i] == player_maker) == 2
            and np.count_nonzero(cur_block[:, i] == 0) == 1
        ):
            total_wins += 1

    # Diagonal checks for both diagonals (main and anti-diagonal)
    # Main diagonal (top-left to bottom-right)
    if (
        np.count_nonzero(
            [cur_block[0][0], cur_block[1][1], cur_block[2][2]] == player_maker
        )
        == 2
        and cur_block[1][1] == 0
    ):
        total_wins += 1

    # Anti-diagonal (top-right to bottom-left)
    if (
        np.count_nonzero(
            [cur_block[0][2], cur_block[1][1], cur_block[2][0]] == player_maker
        )
        == 2
        and cur_block[1][1] == 0
    ):
        total_wins += 1

    # Check for the cross 'X' pattern (as described, when the corners form a cross)
    if (
        cur_block[0][0]
        == cur_block[2][2]
        == cur_block[0][2]
        == cur_block[2][0]
        == player_maker
    ):
        # We already counted diagonal and row/column wins involving this pattern.
        # So, we just need to check that the center is not occupied by the same player.
        if cur_block[1][1] != player_maker:
            total_wins -= 1  # Exclude this case as it is a false positive.

    return total_wins
