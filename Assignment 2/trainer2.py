import tensorflow as tf
import keras
from keras import layers
from keras.models import Model
from keras import models
from keras.optimizers import Adam
import numpy as np
import math
from collections import deque
import os
import time
from datetime import datetime
import h5py
import copy
from state import State_2, UltimateTTT_Move

""" 
Functions for game board
"""
train_episodes = 100
mcts_search = 600
n_pit_network = 20
playgames_before_training = 2
cpuct = 4
training_epochs = 2
learning_rate = 0.001
save_model_path = 'training_dir'
def get_empty_board():
    return State_2()

def print_board(state):
    firstRow = ""
    secondRow = ""
    thirdRow = ""

    totalBoard = state.blocks
    # Takes each board, saves the rows in a variable, then prints the variables
    for boardIndex in range(len(totalBoard)):
        firstRow = firstRow + "|" + " ".join(map(str, totalBoard[boardIndex][0])) + "|"
        secondRow = secondRow + "|" + " ".join(map(str, totalBoard[boardIndex][1])) + "|"
        thirdRow = thirdRow + "|" + " ".join(map(str, totalBoard[boardIndex][2])) + "|"

        # if 3 boards have been collected, then it prints the boards out and resets the variables (firstRow, secondRow, etc.)
        if boardIndex > 1 and (boardIndex + 1) % 3 == 0:
            print(firstRow)
            print(secondRow)
            print(thirdRow)
            print("---------------------")
            firstRow = ""
            secondRow = ""
            thirdRow = ""

def possiblePos(state, subBoard):
    valid_moves = state.get_valid_moves
    if subBoard == 9:
        return range(81)
    return [(move.index_local_board * 9) + (move.x * 3) + move.y for move in valid_moves]

def move(state, action, player):
    index_local_board = action // 9
    x = (action % 9) // 3
    y = action % 3
    move = UltimateTTT_Move(index_local_board, x, y, player)
    state.act_move(move)
    newsubBoard = (x * 3) + y
    return state, newsubBoard, state.game_over

def fill_winning_boards(state):
    new_board = copy.deepcopy(state)
    for i in range(9):
        if state.global_cells[i] == 1:
            new_board.blocks[i] = np.ones((3, 3))
        elif state.global_cells[i] == -1:
            new_board.blocks[i] = -np.ones((3, 3))
    return new_board

def board_to_array(state):
    board = fill_winning_boards(state)
    array = np.zeros((9, 9))
    for i in range(9):
        for x in range(3):
            for y in range(3):
                array[i // 3 * 3 + x, i % 3 * 3 + y] = board.blocks[i][x, y]
    return array

def mcts(s, current_player, mini_board):
    if mini_board == 9:
        possibleA = range(81)
    else:
        possibleA = possiblePos(s, mini_board)

    sArray = board_to_array(s)
    sTuple = tuple(map(tuple, sArray))

    if len(possibleA) > 0:
        if sTuple not in P.keys():
            policy, v = nn.predict(sArray.reshape(1, 9, 9))
            v = v[0][0]
            valids = np.zeros(81)
            np.put(valids, possibleA, 1)
            policy = policy.reshape(81) * valids
            policy = policy / np.sum(policy)
            P[sTuple] = policy

            Ns[sTuple] = 1

            for a in possibleA:
                Q[(sTuple, a)] = 0
                Nsa[(sTuple, a)] = 0
                W[(sTuple, a)] = 0
            return -v

        best_uct = -100
        for a in possibleA:
            uct_a = Q[(sTuple, a)] + cpuct * P[sTuple][a] * (math.sqrt(Ns[sTuple]) / (1 + Nsa[(sTuple, a)]))
            if uct_a > best_uct:
                best_uct = uct_a
                best_a = a

        next_state, mini_board, wonBoard = move(s, best_a, current_player)

        if wonBoard:
            v = 1
        else:
            current_player *= -1
            v = mcts(next_state, current_player, mini_board)
    else:
        return 0

    W[(sTuple, best_a)] += v
    Ns[sTuple] += 1
    Nsa[(sTuple, best_a)] += 1
    Q[(sTuple, best_a)] = W[(sTuple, best_a)] / Nsa[(sTuple, best_a)]
    return -v

def get_action_probs(init_board, current_player, mini_board):
    for _ in range(mcts_search):
        s = copy.deepcopy(init_board)
        value = mcts(s, current_player, mini_board)

    print("done one iteration of MCTS")

    actions_dict = {}

    sArray = board_to_array(init_board)
    sTuple = tuple(map(tuple, sArray))

    for a in possiblePos(init_board, mini_board):
        actions_dict[a] = Nsa[(sTuple, a)] / Ns[sTuple]

    action_probs = np.zeros(81)

    for a in actions_dict:
        np.put(action_probs, a, actions_dict[a], mode='raise')

    return action_probs

def playgame():
    done = False
    current_player = 1
    game_mem = []
    mini_board = 9

    real_board = get_empty_board()

    while not done:
        s = copy.deepcopy(real_board)
        policy = get_action_probs(s, current_player, mini_board)
        policy = policy / np.sum(policy)
        game_mem.append([board_to_array(real_board), current_player, policy, None])
        action = np.random.choice(len(policy), p=policy)

        print("policy ", policy)
        print("chosen action", action)
        print("mini-board", mini_board)
        print_board(real_board)

        next_state, mini_board, wonBoard = move(real_board, action, current_player)

        if len(possiblePos(next_state, mini_board)) == 0:
            for tup in game_mem:
                tup[3] = 0
            return game_mem

        if wonBoard:
            for tup in game_mem:
                if tup[1] == current_player:
                    tup[3] = 1
                else:
                    tup[3] = -1
            return game_mem

        current_player *= -1
        s = next_state

def neural_network():
    input_layer = layers.Input(shape=(9, 9), name="BoardInput")
    reshape = layers.core.Reshape((9, 9, 1))(input_layer)
    conv_1 = layers.Conv2D(128, (3, 3), padding='valid', activation='relu', name='conv1')(reshape)
    conv_2 = layers.Conv2D(128, (3, 3), padding='valid', activation='relu', name='conv2')(conv_1)
    conv_3 = layers.Conv2D(128, (3, 3), padding='valid', activation='relu', name='conv3')(conv_2)

    conv_3_flat = layers.Flatten()(conv_3)

    dense_1 = layers.Dense(512, activation='relu', name='dense1')(conv_3_flat)
    dense_2 = layers.Dense(256, activation='relu', name='dense2')(dense_1)

    pi = layers.Dense(81, activation="softmax", name='pi')(dense_2)
    v = layers.Dense(1, activation="tanh", name='value')(dense_2)

    model = Model(inputs=input_layer, outputs=[pi, v])
    model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate))

    model.summary()
    return model

def train_nn(nn, game_mem):
    print("Training Network")
    print("length of game_mem", len(game_mem))

    state = []
    policy = []
    value = []

    for mem in game_mem:
        state.append(mem[0])
        policy.append(mem[2])
        value.append(mem[3])

    state = np.array(state)
    policy = np.array(policy)
    value = np.array(value)

    history = nn.fit(state, [policy, value], batch_size=32, epochs=training_epochs, verbose=1)

def pit(nn, new_nn):
    print("Pitting networks")
    nn_wins = 0
    new_nn_wins = 0

    for _ in range(n_pit_network):
        s = get_empty_board()
        mini_board = 9

        while True:
            policy, v = nn.predict(board_to_array(s).reshape(1, 9, 9))
            valids = np.zeros(81)

            possibleA = possiblePos(s, mini_board)

            if len(possibleA) == 0:
                break

            np.put(valids, possibleA, 1)
            policy = policy.reshape(81) * valids
            policy = policy / np.sum(policy)
            action = np.argmax(policy)

            next_state, mini_board, win = move(s, action, 1)
            s = next_state

            if win:
                nn_wins += 1
                break

            policy, v = new_nn.predict(board_to_array(s).reshape(1, 9, 9))
            valids = np.zeros(81)

            possibleA = possiblePos(s, mini_board)

            if len(possibleA) == 0:
                break

            np.put(valids, possibleA, 1)
            policy = policy.reshape(81) * valids
            policy = policy / np.sum(policy)
            action = np.argmax(policy)

            next_state, mini_board, win = move(s, action, -1)
            s = next_state

            if win:
                new_nn_wins += 1
                break

    if (new_nn_wins + nn_wins) == 0:
        print("The game was a complete tie")
        now = datetime.utcnow()
        filename = 'tictactoeTie{}.h5'.format(now)
        model_path = os.path.join(save_model_path, filename)
        nn.save(model_path)
        return False

    win_percent = float(new_nn_wins) / float(new_nn_wins + nn_wins)
    if win_percent > 0.52:
        print("The new network won")
        print(win_percent)
        return True
    else:
        print("The new network lost")
        print(new_nn_wins)
        return False

nn = neural_network()

def train():
    global nn
    global Q
    global Nsa
    global Ns
    global W
    global P

    game_mem = []

    for episode in range(train_episodes):
        nn.save('temp.h5')
        old_nn = models.load_model('temp.h5')

        for _ in range(playgames_before_training):
            game_mem += playgame()

        train_nn(nn, game_mem)
        game_mem = []
        if pit(old_nn, nn):
            del old_nn
            Q = {}
            Nsa = {}
            Ns = {}
            W = {}
            P = {}
        else:
            nn = old_nn
            del old_nn

    now = datetime.utcnow()
    filename = 'tictactoe_MCTS200{}.h5'.format(now)
    model_path = os.path.join(save_model_path, filename)
    nn.save(model_path)

train()