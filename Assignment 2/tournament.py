import subprocess

# Khởi tạo thống kê
results = {"X": 0, "O": 0, "draw": 0}

# Chạy n vòng đấu
for i in range(5):
    print(f"Running game {i + 1}...")
    # Chạy main.py bằng subprocess và thu thập kết quả từ stdout
    result = subprocess.run(
        ["python", "main.py"], capture_output=True, text=True
    )

    # Tìm dòng chứa kết quả trận đấu
    output_lines = result.stdout.splitlines()
    for line in output_lines:
        if "winner:" in line:  # Kiểm tra xem có dòng nào thông báo kết quả không
            winner = line.split(":")[-1].strip()  # Lấy phần thắng (X, O hoặc draw)
            if winner in results:
                results[winner] += 1
            else:
                print(f"Unexpected result in game {i + 1}: {winner}")
            break
    else:
        results["draw"] += 1

# In thống kê kết quả
print("\nTournament Results:")
print(f"Player X Wins: {results['X']}")
print(f"Player O Wins: {results['O']}")
print(f"Draws: {results['draw']}")