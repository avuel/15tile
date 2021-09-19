def h(grid: list):
    sum: int = 0
    for i in range(len(grid)):
        row = i // 4
        col = i % 4
        end_row = grid[i] // 4
        end_col = grid[i] % 4
        sum += (row - end_row) + (col - end_col)
    
    return sum