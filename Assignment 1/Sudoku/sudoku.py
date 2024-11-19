from time import time
import numpy as np

np.random.seed(0)
mutation_rate_default = 0.1

# Biểu diễn một ứng viên trong quần thể 
class Candidate:
    def __init__(self):
        self.puzzle = np.zeros((9, 9), dtype=int)
        self.fitness = 0.0
        
    # Phương thức sử dụng để đánh giá mức độ phù hợp của mỗi ứng viên trong quần thể giải Sudoku
    # tính hợp lệ của mỗi ứng viên được tính dựa trên số lượng các số từ 1 đến 9 trong các hàng, cột và khối 3x3
    def update_fitness(self):
        # Khởi tạo các mảng đếm số lần xuất hiện của các số 1-9 trong mỗi hàng, cột và khối 3x3
        row = np.zeros(9)
        column = np.zeros(9)
        block = np.zeros(9)
        
        row_sum = 0
        column_sum = 0
        block_sum = 0
        
        # Duyệt qua từng hàng, cột và đếm số lần xuất hiện của các số 1-9 trong mỗi hàng, cột
        for i in range(9):
            for j in range(9):
                row[self.puzzle[i][j] - 1] += 1
                column[self.puzzle[j][i] - 1] += 1
                
            # Tính điểm của mỗi hàng, cột dựa trên số lượng các số duy nhất trong hàng và cột đó
            # Nếu hàng hoặc cột có đủ các số từ 1 đến 9 không trùng lặp, điểm sẽ đạt giá trị tối đa là 1/9
            row_sum += (1.0/len(set(row))) / 9
            column_sum += (1.0/len(set(column))) / 9
            
            # Đặt lại bộ đếm
            row = np.zeros(9)
            column = np.zeros(9)
            
        # Tính điểm lượng giá cho các block 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                for k in range(3):
                    for l in range(3):
                        block[self.puzzle[i + k][j + l] - 1] += 1
                block_sum += (1.0/len(set(block))) / 9
                block = np.zeros(9)
            
        # Nếu row_sum, column_sum, và block_sum đều đạt giá trị 1 (tức là mỗi hàng, cột và khối đều có các số từ 1 đến 9 không trùng lặp)
        # thì giá trị fitness = 1.0 => đây là một lời giải hoàn chỉnh và hợp lệ cho bài toán Sudoku
        if int(row_sum) == 1 and int(column_sum) == 1 and int(block_sum) == 1:
            self.fitness = 1.0
        # Nếu không, giá trị fitness bằng tích các điểm lượng giá
        else:
            self.fitness = row_sum * column_sum * block_sum     
    
    # Phương thức sử dụng để thực hiện đột biến trên một ứng viên của quần thể Sudoku
    # Thay đổi được thực hiện bằng cách chọn một hàng và hoán đổi 2 giá trị trong hàng đó
    def mutate(self, mutate_rate, given_puzzle):   
        mutate = False
        # Kiểm tra xác suất đột biến: Nếu một giá trị ngẫu nhiên từ 0 đến 1 nhỏ hơn mutation_rate, thì sẽ tiến hành đột biến.
        if np.random.uniform(0, 1) < mutate_rate: 
            while not mutate:
                # Chọn một hàng ngẫu nhiên để hoán đổi
                row1 = np.random.randint(0, 9)
                row2 = row1
                
                # Chọn ngẫu nhiên 2 cột khác nhau trong hàng để hoán đổi
                from_column , to_column = np.random.choice(range(9), size=2 ,replace=False)
                # Kiểm tra xem cả hai ô được chọn có trống trong bảng given_puzzle hay không để đảm bảo rằng các ô cố định (đã được điền trong đề bài) sẽ không bị thay đổi
                if given_puzzle.puzzle[row1][from_column] == 0 and given_puzzle.puzzle[row1][to_column] == 0:
                    # kiểm tra xem việc hoán đổi có tạo ra trùng lặp nào trong cột hoặc khối 3x3 hay không
                    if not(given_puzzle.is_column_duplicate(to_column, self.puzzle[row1][from_column]) 
                        or given_puzzle.is_column_duplicate(from_column, self.puzzle[row2][to_column])
                        or given_puzzle.is_block_duplicate(row2, to_column, self.puzzle[row1][from_column])
                        or given_puzzle.is_block_duplicate(row1, from_column, self.puzzle[row2][to_column])):
                        
                        # Thực hiện hoán đổi
                        temp = self.puzzle[row1][from_column]
                        self.puzzle[row1][from_column] = self.puzzle[row2][to_column]
                        self.puzzle[row2][to_column] = temp
                        mutate = True
        
        return mutate

# Lớp con của candidate, đại diện cho bảng sudoku đã cho với một số ô được điền trước
class GivenPuzzle(Candidate):
    def __init__(self, puzzle):
        self.puzzle = puzzle
    
    # Phương thức  kiểm tra xem có giá trị trùng lặp trong một hàng cụ thể không
    def is_row_duplicate(self, row, value):
        return value in self.puzzle[row]
    
    # Phương thức kiểm tra xem có giá trị trùng lặp trong một cột cụ thể không
    def is_column_duplicate(self, column, value):
        return value in [row[column] for row in self.puzzle]
    
    # Phương thức kiểm tra xem có giá trị trùng lặp trong một block 3x3 cụ thể không
    def is_block_duplicate(self, row, column, value):
        i = 3 * (row // 3)
        j = 3 * (column // 3)
        
        block_values = [self.puzzle[i + m][j + n] for m in range(3) for n in range(3)]
        return value in block_values
    
# Biểu diễn cho quần thể gồm các ứng viên
class Population(object):
    def __init__(self):
        self.candidates = []
    
    # Phương thức sử dụng để tạo ra một quần thể mới dựa trên bảng Sudoku đã cho
    def seed(self, size, given_puzzle):
        self.candidates = []
        
        print (" Seeding population ... ")
        
        # Tính toán tập hợp các giá trị hợp lệ cho mỗi ô trống và lưu vào legal_values
        legal_values = [[[value for value in range(1, 10) if
                  self.is_legal(given_puzzle, row, col, value)]
                  for col in range(9)] for row in range(9)]
        
        # Tạo quần thể với các ứng viên mới
        for _ in range(size):
            candidate = Candidate()
            # Xây dựng các hàng cho từng ứng viên
            for i in range(9):
                if np.count_nonzero(given_puzzle.puzzle[i]) == 9:
                    # Nếu hàng đã được điền đầy đủ trong bảng đầu vào, ta chỉ cần copy lại nó
                    candidate.puzzle.append(given_puzzle.puzzle[i])
                    continue
                
                # Điền giá trị cho các ô trống trong hàng
                row = np.zeros(9) # Mảng chứa các giá trị cho hàng i
                for j in range(9):
                    # Nếu ô (i,j) đã có giá trị trong given puzzle, nó sẽ được sao chép lại
                    if given_puzzle.puzzle[i][j] > 0:
                        row[j] = given_puzzle.puzzle[i][j]
                    # Nếu không, sinh ra một giá trị hợp lệ ngẫu nhiên được chọn từ legal_values để điền vào ô trống
                    else:
                        values_set = legal_values[i][j] if len(legal_values[i][j]) > 0 else range(1, 10)
                        row[j] = np.random.choice(values_set)

                # Đảm bảo không có các giá trị trùng lặp trong hàng
                # Sau khi điền xong các giá trị cho hàng, chương trình kiểm tra xem hàng đó có chứa đủ các số từ 1 đến 9 mà không bị trùng lặp hay không
                # Nếu có trùng lặp, các ô chưa điền sẵn (<= 0) sẽ được thay thế ngẫu nhiên cho đến khi hàng không còn trùng lặp
                while len(np.unique(row)) != 9:
                    for j in range(9):
                        if given_puzzle.puzzle[i][j] <= 0:
                            values_set = legal_values[i][j] if len(legal_values[i][j]) > 0 else range(1, 10)
                            row[j] = np.random.choice(values_set)

                candidate.puzzle[i] = row.astype(int)
            self.candidates.append(candidate)
        
        self.update_fitness()
        
    # Phương thức cập nhật giá trị fitness cho từng ứng viên
    def update_fitness(self):
        for candidate in self.candidates:
            candidate.update_fitness()
        
    # Phương thức kiểm tra xem việc đặt một giá trị vào một ô cụ thể trên bảng Sudoku có vi phạm các quy tắc không
    def is_legal(self, puzzle, row, col, value):
        return (not puzzle.is_column_duplicate(col, value)
                and not puzzle.is_row_duplicate(row, value)
                and not puzzle.is_block_duplicate(row, col, value))
        
    # Sắp xếp thứ tự các ứng viên trong quần thể theo giá trị fitness
    def sort(self):
        self.candidates.sort(key=lambda x: x.fitness, reverse=True)
    
# Biểu diễn cho một vòng đấu trong quần thể để lựa chọn ứng viên cho quá trình lai ghép.
class Tournament:
    def __init__(self): pass
    
    def compete(self, candidates):
        # Chọn ngẫu nhiên 2 ứng viên từ quần thể và cho chúng đấu với nhau
        candidate1, candidate2 = np.random.choice(candidates, size=2, replace=False)
        
        # Lấy giá trị fitness của 2 ứng viên
        fitness1 = candidate1.fitness
        fitness2 = candidate2.fitness
        
        # Xác định ứng viên mạnh nhất và yếu nhất dựa trên giá trị fitness
        fittest = candidate1 if fitness1 > fitness2 else candidate2
        weakest = candidate1 if fitness1 < fitness2 else candidate2
        
        selection_rate = 0.8 # Tỷ lệ lựa chọn: Xác suất chọn ứng viên mạnh nhất
        
        #  tạo giá trị ngẫu nhiên từ phân phối đều trong khoảng từ 0 đến 1 để quyết định ứng viên nào sẽ được lựa chọn.
        value = np.random.uniform(0, 1)
        
        # Thực hiện lựa chọn dựa trên tỷ lệ lựa chọn
        return fittest if value  < selection_rate else weakest
    
# Lớp thực hiện việc lai ghép giữa các ứng viên để tạo ra ứng viên mới   
class Crossover:
    def crossover(self, parent1, parent2, crossover_rate):
        # Tạo 2 ứng viên con bằng cách lai ghép các gen cha mẹ
        child1 = Candidate()
        child2 = Candidate()
        
        # Tạo bản sao của gen cha mẹ
        child1.puzzle = np.copy(parent1.puzzle)
        child2.puzzle = np.copy(parent2.puzzle)
        
        # Thực hiện lai ghép
        if np.random.uniform(0 , 1) < crossover_rate:
            # Chọn điểm lai ghép ngẫu nhiên (0 - 8), đảm bảo rằng có ít nhất 1 hàng được chọn
            crossover_point1 = np.random.randint(0, 8)
            crossover_point2 = np.random.randint(crossover_point1, 9)
            
            # Lặp qua từng hàng trong phạm vi point 1 tới point 2 và thực hiện lai ghép gen của hai cha mẹ ở các hàng này
            for i in range(crossover_point1, crossover_point2):
                child1.puzzle[i], child2.puzzle[i] = self.crossover_rows(child1.puzzle[i], child2.puzzle[i])
                
        return child1, child2
      
    # Phương thức hỗ trợ thực hiện lai ghép gene giữa các hàng của 2 gen cha mẹ     
    def crossover_rows(self, row1, row2):
        child1 = np.zeros(9)
        child2 = np.zeros(9)
        
        remaining = list(range(1, 10)) # Danh sách chứa các số từ 1 đến 9, giúp theo dõi các số chưa được sử dụng trong các hàng con
        cycle = 0 # Biến đếm chu kỳ để xác định luân phiên giữa các giá trị lấy từ cha mẹ 1 và cha mẹ 2
        
        # Lặp cho đến khi tất cả ô trong 2 con đều được điền
        while (0 in child1) and (0 in child2):
            if cycle % 2 == 0:
                # Thực hiện chu kỳ chẵn, gán giá trị từ gen cha mẹ 1
                # Tìm một giá trị chưa được sử dụng trong hàng tương ứng của cha mẹ 1
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child1[index] = row1[index]
                child2[index] = row2[index]
                next_value = row2[index]
                
                # Thực hiện chu kỳ hoán đổi
                while next_value != start:
                    index = self.find_value(row1, next_value)
                    child1[index] = row1[index]
                    remaining.remove(row1[index])
                    child2[index] = row2[index]
                    next_value = row2[index]
                
                cycle += 1
            else:
                # Thực hiện chu kỳ chẵn, gán giá trị từ gen cha mẹ 1
                # Tìm một giá trị chưa được sử dụng trong hàng tương ứng của cha mẹ 1
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child1[index] = row2[index]
                child2[index] = row1[index]
                next_value = row2[index]
                
                # Thực hiện chu kỳ hoán đổi
                while next_value != start:
                    index = self.find_value(row1, next_value)
                    child1[index] = row2[index]
                    remaining.remove(row1[index])
                    child2[index] = row1[index]
                    next_value = row2[index]
                
                cycle += 1
        
        return child1, child2
    
    # Phương thức hỗ trợ tìm kiếm giá trị chưa sử dụng trong hàng
    def find_unused(self, row, remaining):
        for i in range(9):
            if row[i] in remaining:
                return i
    
    # Phương thức tìm kiếm index của một giá trị trong hàng
    def find_value(self, row, value):
        for i in range(9):
            if row[i] == value:
                return i

class Sudoku:
    def __init__(self, size = 1000, generations = 1000, mutation_rate = mutation_rate_default):
        self.given_puzzle = None # Bảng Sudoku ban đầu mà chương trình cần giải
        self.population = None # Quần thể hiện tại của các ứng viên
        self.best_candidate = None # Ứng viên tốt nhất tại một thời điểm trong quá trình tiến hóa
        self.size = size # Kích thước của quần thể: biểu diễn số lượng ứng viên của quần thể tại mỗi thế hệ
        self.generations = generations # Số thế hệ tối đa cho quá trình tiến hóa
        self.mutation_rate = mutation_rate # Xác suất xảy ra đột biến
        
        self.num_elites = int(0.05*self.size) # Số lượng ứng viên ưu tú được giữ lại từ thế hệ này sang thế hệ khác
        self.reseeding_threshold = 100 # Ngưỡng để tái khởi động một phần hoặc toàn bộ quần thể
        
        # Dùng để điều chỉnh xác suất đột biến theo Quy tắc 1/5 của Richenberg
        self.num_mutations = 0 # Số đột biến đã xảy ra
        self.phi = 0 # Số đột biến thành công
        self.sigma = 1
        
        self.cycle_crossover = Crossover()
        self.tournament = Tournament()
        
    # Phương thức dùng để load bảng Sudoku đã cho từ đề bài
    def load_puzzle(self, puzzle):
        self.given_puzzle = GivenPuzzle(puzzle)
    
    # Phương thức triển khai giải thuật di truyền để giải bài toán Sudoku
    def solve(self):
        # Khởi tạo quần thể ban đầu
        self.population = Population()
        self.population.seed(self.size, self.given_puzzle)
        
        # Lặp qua các thế hệ
        stale = 0 #  Biến đếm số thế hệ liên tiếp mà quần thể không cải thiện về fitness
        for generation in range(0, self.generations):
            print("Generation ", generation)
            
            # Trong mỗi thế hệ, chọn ra ứng viên tốt nhất và kiểm tra đã tìm thấy lời giải hay chưa
            best_fitness = 0.0
            for candidate in range(0, self.size):
                fitness = self.population.candidates[candidate].fitness
                if fitness == 1:
                    print("Solution found at generation ", generation)
                    print(self.population.candidates[candidate].puzzle)
                    return self.population.candidates[candidate]
                
                # Tìm ứng viên tốt nhất
                if fitness > best_fitness:
                    best_fitness = fitness
                    self.best_candidate = self.population.candidates[candidate]
                
            print("Best fitness: ", best_fitness)
            print("Stale: ", stale)
            
            # Tạo quần thể kế tiếp
            next_population = []
            # Lựa chọn các cá thể ưu tú (elite) để giữ lại cho thế hệ kế tiếp
            self.population.sort()
            elites = []
            for idx in range(0, self.num_elites):
                elite = Candidate()
                elite.puzzle = np.copy(self.population.candidates[idx].puzzle)
                elites.append(elite)
            
            # Tạo các ứng viên còn lại bằng lai ghép
            for _ in range(self.num_elites, self.size, 2):
                parent1 = self.tournament.compete(self.population.candidates)
                parent2 = self.tournament.compete(self.population.candidates)
                child1, child2 = self.cycle_crossover.crossover(parent1, parent2, crossover_rate=0.9)
                
                # Đột biến cá thể con 1
                old_fitness = child1.fitness
                mutate = child1.mutate(self.mutation_rate, self.given_puzzle)
                child1.update_fitness()
                if mutate:
                    self.num_mutations += 1
                    if child1.fitness > old_fitness: # Dùng để theo dõi tỷ lệ thành công của đột biến
                        self.phi += 1
                
                # Đột biến cá thể con 2
                old_fitness = child2.fitness
                mutate = child2.mutate(self.mutation_rate, self.given_puzzle)
                child2.update_fitness()
                if mutate:
                    self.num_mutations += 1
                    if child2.fitness > old_fitness: # Dùng để theo dõi tỷ lệ thành công của đột biến
                        self.phi += 1
                        
                # Thêm các cá thể con vào quần thể kế tiếp
                next_population.append(child1)
                next_population.append(child2)
                
            # Thêm các cá thể ưu tú vào quần thể kế tiếp
            for elite in range(0, self.num_elites):
                next_population.append(elites[elite])
                
            # Chọn thế hệ kế tiếp
            self.population.candidates = next_population
            self.population.update_fitness()
            
            # Điều chỉnh tỷ lệ đột biến (Sử dụng Quy tắc 1/5 của Rechenberg)
            if self.num_mutations == 0:
                self.phi = 0 # Tránh chia cho 0
            else: 
                self.phi = self.phi / self.num_mutations
            
            if self.phi > 0.2:
                self.sigma = self.sigma / 0.998
            elif self.phi < 0.2:
                self.sigma = self.sigma * 0.998
            
            self.mutation_rate = abs(np.random.normal(loc=0.0, scale=self.sigma, size=None))
            self.num_mutations = 0
            self.phi = 0
            
            # Kiểm tra quần thể bị "stale"
            if self.population.candidates[0].fitness != self.population.candidates[1].fitness:
                stale = 0
            else:
                stale += 1
            # Nếu stale vượt ngưỡng (sau N thế hệ liên tiếp không có sự cải thiện) quần thể sẽ được tái khởi tạo
            if stale >= self.reseeding_threshold:
                print("The population has gone stale. Re-seeding ...")
                self.population.seed(self.size, self.given_puzzle)
                stale = 0
                self.sigma = 1
                self.phi = 0
                self.num_mutations = 0
                self.mutation_rate = mutation_rate_default
        
        # Kết thúc giải thuật nếu không tìm thấy lời giải
        print("No solution found.")
        return None
            

def readInput(filename):
    given_puzzle = []
    with open(filename, "r") as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            given_puzzle.append(row)
    return given_puzzle


def writeOutput(filename, execution_time, solution):
    with open(filename, 'w') as file:
        # Ghi ma trận Sudoku đã giải
        file.write("Sudoku solution:\n")
        for row in solution:
            file.write(" ".join(map(str, row)) + "\n")
        
        # Ghi thời gian thực thi
        file.write(f"\nExecution time: {execution_time:.4f} seconds\n")
    
def main():
    # Đọc bài toán từ file input
    given_puzzle = readInput("input.txt")
    output_file = "output.txt"
    print("Loading...")
    
    # Khởi tạo đối tượng Sudoku và gán bảng đầu vào
    sudoku_solver = Sudoku()
    sudoku_solver.load_puzzle(given_puzzle)
    
    # Bắt đầu giải thuật và đo thời gian thực thi
    start_time = time()
    solution_candidate = sudoku_solver.solve()
    end_time = time()

    # Tính thời gian thực thi
    execution_time = end_time - start_time

    # Ghi kết quả ra file output
    if solution_candidate:
        solution = solution_candidate.puzzle  # Lấy ma trận Sudoku đã giải
        writeOutput("output.txt", execution_time, solution)

    return execution_time

if __name__ == "__main__":
    main()
