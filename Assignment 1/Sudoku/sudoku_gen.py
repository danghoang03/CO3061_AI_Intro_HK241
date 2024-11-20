# -*- coding: utf-8 -*-
import time
import copy
import random

class cell():
    def __init__(self, position):
        self.possibleAnswers = [1,2,3,4,5,6,7,8,9]
        self.answer = None
        self.position = position
        self.solved = False
        
    def remove(self, num):
        if num in self.possibleAnswers and self.solved == False:
            self.possibleAnswers.remove(num)
            if len(self.possibleAnswers) == 1:
                self.answer = self.possibleAnswers[0]
                self.solved = True
        if num in self.possibleAnswers and self.solved == True:
            self.answer = 0

    def solvedMethod(self):
        return self.solved

    def checkPosition(self):
        return self.position

    def returnPossible(self):
        return self.possibleAnswers

    def lenOfPossible(self):
        return len(self.possibleAnswers)

    def returnSolved(self):
        if self.solved == True:
            return self.possibleAnswers[0]
        else:
            return 0
        
    def setAnswer(self, num):
        if num in [1,2,3,4,5,6,7,8,9]:
            self.solved = True
            self.answer = num
            self.possibleAnswers = [num]
        else:
            raise(ValueError)
       
    def reset(self):
        self.possibleAnswers = [1,2,3,4,5,6,7,8,9]
        self.answer = None
        self.solved = False

def emptySudoku():
    ans = []
    for x in range(1,10):
        if x in [7,8,9]:
            intz = 7
            z = 7
        if x in [4,5,6]:
            intz = 4
            z = 4
        if x in [1,2,3]:
            intz = 1
            z = 1
        for y in range(1,10):
            z = intz
            if y in [7,8,9]:
                z += 2
            if y in [4,5,6]:
                z += 1
            if y in [1,2,3]:
                z += 0
            c = cell((x,y,z))
            ans.append(c)
    return ans 

def printSudoku(sudoku, filename):
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row8 = []
    row9 = []
    for i in range(81):
        if i in range(0,9):
            row1.append(sudoku[i].returnSolved())
        if i in range(9,18):
            row2.append(sudoku[i].returnSolved())
        if i in range(18,27):
            row3.append(sudoku[i].returnSolved())
        if i in range(27,36):
            row4.append(sudoku[i].returnSolved())
        if i in range(36,45):
            row5.append(sudoku[i].returnSolved())
        if i in range(45,54):
            row6.append(sudoku[i].returnSolved())
        if i in range(54,63):
            row7.append(sudoku[i].returnSolved())
        if i in range(63,72):
            row8.append(sudoku[i].returnSolved())
        if i in range(72,81):
            row9.append(sudoku[i].returnSolved())
    output = []
    output.append(" ".join(map(str, row1[0:3])) + " " + " ".join(map(str, row1[3:6])) + " " + " ".join(map(str, row1[6:9])))
    output.append(" ".join(map(str, row2[0:3])) + " " + " ".join(map(str, row2[3:6])) + " " + " ".join(map(str, row2[6:9])))
    output.append(" ".join(map(str, row3[0:3])) + " " + " ".join(map(str, row3[3:6])) + " " + " ".join(map(str, row3[6:9])))
    output.append(" ".join(map(str, row4[0:3])) + " " + " ".join(map(str, row4[3:6])) + " " + " ".join(map(str, row4[6:9])))
    output.append(" ".join(map(str, row5[0:3])) + " " + " ".join(map(str, row5[3:6])) + " " + " ".join(map(str, row5[6:9])))
    output.append(" ".join(map(str, row6[0:3])) + " " + " ".join(map(str, row6[3:6])) + " " + " ".join(map(str, row6[6:9])))
    output.append(" ".join(map(str, row7[0:3])) + " " + " ".join(map(str, row7[3:6])) + " " + " ".join(map(str, row7[6:9])))
    output.append(" ".join(map(str, row8[0:3])) + " " + " ".join(map(str, row8[3:6])) + " " + " ".join(map(str, row8[6:9])))
    output.append(" ".join(map(str, row9[0:3])) + " " + " ".join(map(str, row9[3:6])) + " " + " ".join(map(str, row9[6:9])))
    print("\n".join(output))
    save_to_file(output, filename)

def sudokuGen():
    cells = [i for i in range(81)]
    sudoku = emptySudoku()
    # backtrack_generate(sudoku)
    while len(cells) != 0:
        lowestNum = []
        Lowest = []
        for i in cells:
            lowestNum.append(sudoku[i].lenOfPossible())
        m = min(lowestNum)
        for i in cells:
            if sudoku[i].lenOfPossible() == m:
                Lowest.append(sudoku[i])
        choiceElement = random.choice(Lowest)
        choiceIndex = sudoku.index(choiceElement) 
        cells.remove(choiceIndex)                 
        position1 = choiceElement.checkPosition()
        if choiceElement.solvedMethod() == False:
            possibleValues = choiceElement.returnPossible()
            finalValue = random.choice(possibleValues)
            choiceElement.setAnswer(finalValue)
            for i in cells:
                position2 = sudoku[i].checkPosition()
                if position1[0] == position2[0]:
                    sudoku[i].remove(finalValue)
                if position1[1] == position2[1]:
                    sudoku[i].remove(finalValue)
                if position1[2] == position2[2]:
                    sudoku[i].remove(finalValue)
        else:
            finalValue = choiceElement.returnSolved()
            for i in cells:
                position2 = sudoku[i].checkPosition()
                if position1[0] == position2[0]:
                    sudoku[i].remove(finalValue)
                if position1[1] == position2[1]:
                    sudoku[i].remove(finalValue)
                if position1[2] == position2[2]:
                    sudoku[i].remove(finalValue)
    return sudoku

def backtrack_generate(sudoku):
    """Sử dụng backtracking để sinh ra bảng Sudoku hoàn chỉnh."""
    for i in range(81):
        if sudoku[i].returnSolved() == 0:  # Nếu ô hiện tại chưa có số
            row, col = i // 9, i % 9
            numbers = list(range(1, 10))
            random.shuffle(numbers)  # Xáo trộn thứ tự số để tạo tính ngẫu nhiên

            for num in numbers:
                if is_valid(sudoku, row, col, num):
                    sudoku[i].setAnswer(num)

                    # Đệ quy gọi lại hàm để điền ô tiếp theo
                    if backtrack_generate(sudoku):
                        return True

                    # Quay lui nếu không tìm được lời giải
                    sudoku[i].reset()

            return False  # Không có số hợp lệ nào để điền vào ô này
    return True

def perfectSudoku():
    result = False
    while result == False:
        s = sudokuGen() 
        result = sudokuChecker(s)
    return s

def sudokuChecker(sudoku):
    for i in range(len(sudoku)):
        for n in range(len(sudoku)):
            if i != n:
                position1 = sudoku[i].checkPosition()
                position2 = sudoku[n].checkPosition()
                if position1[0] == position2[0] or position1[1] == position2[1] or position1[2] == position2[2]:
                    num1 = sudoku[i].returnSolved()
                    num2 = sudoku[n].returnSolved()
                    if num1 == num2:
                        return False
    return True

def is_valid(sudoku, row, col, num):
    # Kiểm tra hàng và cột
    for i in range(9):
        if sudoku[row * 9 + i].returnSolved() == num:
            return False
        if sudoku[i * 9 + col].returnSolved() == num:
            return False
    # Kiểm tra ô 3x3
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if sudoku[(box_row + i) * 9 + (box_col + j)].returnSolved() == num:
                return False
    return True

def solve_sudoku(sudoku):
    for i in range(81):
        if sudoku[i].returnSolved() == 0:  # Ô trống
            row, col = i // 9, i % 9
            for num in range(1, 10):
                if is_valid(sudoku, row, col, num):
                    sudoku[i].setAnswer(num)
                    if solve_sudoku(sudoku):
                        return True
                    sudoku[i].reset()  # Quay lui nếu không tìm được lời giải
            return False
    return True

def count_solutions(sudoku):
    sudoku_copy = copy.deepcopy(sudoku)
    return solve_and_count(sudoku_copy, 0)

def solve_and_count(sudoku, count):
    for i in range(81):
        if sudoku[i].returnSolved() == 0:
            row, col = i // 9, i % 9
            for num in range(1, 10):
                if is_valid(sudoku, row, col, num):
                    sudoku[i].setAnswer(num)
                    count = solve_and_count(sudoku, count)
                    sudoku[i].reset()
            return count
    return count + 1

def remove_cells(sudoku, num_holes, difficulty):
    attempts = num_holes
    while attempts > 0:
        index = random.randint(0, 80)
        if sudoku[index].returnSolved() == 0:  # Nếu đã là ô trống thì tiếp tục
            continue

        # Lưu giá trị hiện tại
        temp = sudoku[index].returnSolved()
        sudoku[index].reset()  # Xóa giá trị hiện tại

        # Đảm bảo vẫn có đúng một lời giải
        if (difficulty != "INSANE"):
            if count_solutions(sudoku) != 1:
                sudoku[index].setAnswer(temp)  # Khôi phục nếu không có duy nhất 1 lời giải
            else:
                attempts -= 1
        else: attempts -= 1

def generate_sudoku(sudoku, difficulty):
    if difficulty == "EASY":
        num_holes = random.randint(30, 35)
    elif difficulty == "MEDIUM":
        num_holes = random.randint(36, 45)
    elif difficulty == "HARD":
        num_holes = random.randint(46, 55)
    elif difficulty == "INSANE":
        num_holes = random.randint(56, 64)
    else:
        raise ValueError("Invalid difficulty level")

    remove_cells(sudoku, num_holes, difficulty)
    return sudoku

def save_to_file(file_content, filename):
    with open(filename, 'w') as f:
        f.write("\n".join(file_content))

def main(level):
    # t1 = time.time()
    print("Perfect Random Sudoku")
    p = perfectSudoku()
    # print(type(p))
    # t2 = time.time()
    # t3 = t2 - t1
    # print("Thời gian chạy là " + str(t3) + " giây")
    printSudoku(p, "expected.txt")
    print("Sudoku Puzzle Generated")
    gsp = generate_sudoku(p, level)
    printSudoku(gsp, "input.txt")