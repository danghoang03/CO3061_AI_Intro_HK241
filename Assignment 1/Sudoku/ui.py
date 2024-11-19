from sys import exit
import pygame
from sudoku import main as Sudoku
from sudoku_gen import main as sudoku_gen

pygame.init()

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def valid(board, pos, num):
    """
    Checks if placing a number at a given position is valid.

    Args:
        board (list[list[int]]): A 9x9 sudoku board.
        pos (tuple[int, int]): The (row, col) position to check.
        num (int): The number to place.

    Returns:
        bool: True if the number can be placed, False otherwise.
    """
    row, col = pos

    # Check row
    if num in board[row]:
        return False

    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 box
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False

    return True

def valid_board(board):
    """
    Validates the initial board for correct dimensions and values.

    Args:
        board (list[list[int]]): A 9x9 sudoku board.

    Returns:
        bool: True if the board is valid, False otherwise.
    """
    if len(board) != 9 or any(len(row) != 9 for row in board):
        return False

    for row in board:
        for num in row:
            if not (0 <= num <= 9):
                return False

    return True

def get_board():
    board = []
    with open("input.txt", 'r') as file:
        for line in file:
            board.append(list(map(int, line.strip().split())))
    if not valid_board(board):
        raise ValueError("The input board is invalid.")
    return board

class Board:
    def __init__(self, window):
        self.board = get_board()
        self.tiles = [
            [Tile(self.board[i][j], window, j * 60, i * 60) for j in range(9)]
            for i in range(9)
        ]
        self.window = window

    def draw_board(self, level=""):
        for i in range(9):
            for j in range(9):
                # draw vertical lines every 3rd column
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (j // 3 * 180, 0), (j // 3 * 180, 540), 4)
                # draw horizontal lines every 3rd row
                if i % 3 == 0 and i != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (0, i // 3 * 180), (540, i // 3 * 180), 4)
                # draw tiles
                self.tiles[i][j].draw((0, 0, 0), 1)
                # display numbers if it is not 0
                if self.tiles[i][j].value != 0:
                    self.tiles[i][j].display(self.tiles[i][j].value, (j * 60 + 21, i * 60 + 16), (0, 0, 0))
        # draw last horizontal lines
        pygame.draw.line(self.window, (0, 0, 0), (0, (i + 1) // 3 * 180), (540, (i + 1) // 3 * 180), 4)
        # draw the level of difficulty
        font = pygame.font.SysFont("Bahnschrift", 32)
        text = font.render(level, True, (0, 0, 0))
        if level == "HARD":
            self.window.blit(text, (450, 555))
        elif level == "MEDIUM":
            self.window.blit(text, (415, 555))
        elif level == "EASY":
            self.window.blit(text, (460, 555))
    
    def redraw(self, time, level):
        self.window.fill((255, 255, 255))
        self.draw_board(level)

        # display the current time elapsed as a number
        font = pygame.font.SysFont("Bahnschrift", 32)
        text = font.render("Time: " + str(time), True, (0, 0, 0))
        self.window.blit(text, (5, 555))
        pygame.display.flip()  # update the game window

    def solve(self, time, level):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True
        
        row, col = empty
        for num in range(1, 10):
            if valid(self.board, (row, col), num):
                self.board[row][col] = num
                self.tiles[row][col].value = num
                self.redraw(time, level)
                if self.solve(time, level):
                    return True
                self.board[row][col] = 0
                self.tiles[row][col].value = 0
                self.redraw(time, level)

class Tile:
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, pos, color):
        font = pygame.font.SysFont(None, 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, pos)

class Menu:
    def __init__(self, window):
        self.window = window
        self.options = ["EASY", "MEDIUM", "HARD"]
        self.selected_index = 0

    def draw(self):
        self.window.fill((255, 255, 255))
        font = pygame.font.SysFont("Bahnschrift", 42)
        title_font = pygame.font.SysFont("Bahnschrift", 64)

        # Title
        title_text = title_font.render("Sudoku", True, (0, 0, 0))
        self.window.blit(title_text, (164, 100))

        # Menu options
        for idx, option in enumerate(self.options):
            color = (0, 0, 255) if idx == self.selected_index else (0, 0, 0)
            text = font.render(option, True, color)
            self.window.blit(text, (190, 240 + idx * 70))

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_index]
        return None

def main():
    # Initialize window
    screen = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    screen.fill((255, 255, 255))
    pygame.display.flip()

    # Initialize variables
    current_screen = "menu"
    menu = Menu(screen)
    board = None
    passed_time = "None"
    solved = False
    level = "EASY"

    # Main game loop
    while True:
        if current_screen == "menu":
            menu.draw()
            level_selected = menu.handle_input()
            if level_selected:
                level = level_selected
                sudoku_gen(level)
                board = Board(screen)
                current_screen = "game"
                solved = False

        elif current_screen == "game":
            board.redraw(passed_time, level)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Solve puzzle
                        passed_time = round(Sudoku(), 4)
                        board.solve(passed_time, level)
                        solved = True
                    elif event.key == pygame.K_ESCAPE:  # Back to menu
                        current_screen = "menu"
                        passed_time = "None"

            # End game condition
            if solved:
                # Handle post-solve behavior if needed
                pass

main()
pygame.quit()