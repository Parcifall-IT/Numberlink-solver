import random
from collections import deque

def neighbors(i, j, M, N):
    """Возвращает координаты соседей клетки (i, j) в пределах матрицы размером MxN."""
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(i + di, j + dj) for di, dj in deltas if 0 <= i + di < M and 0 <= j + dj < N]

def generate_random_paths(M, N, K):
    """Генерирует K случайных путей, полностью покрывающих поле MxN."""
    grid = [[0 for _ in range(N)] for _ in range(M)]
    path_id = 1

    for _ in range(K):
        if path_id > K:
            break
        # Генерируем стартовую точку
        while True:
            start_x, start_y = random.randint(0, M - 1), random.randint(0, N - 1)
            if grid[start_x][start_y] == 0:
                break

        path = [(start_x, start_y)]
        grid[start_x][start_y] = path_id

        while len(path) < (M * N) // K + (1 if path_id <= (M * N) % K else 0):
            current_x, current_y = path[-1]
            random.shuffle(neighbors(current_x, current_y, M, N))
            found_next = False
            for nx, ny in neighbors(current_x, current_y, M, N):
                if grid[nx][ny] == 0:
                    grid[nx][ny] = path_id
                    path.append((nx, ny))
                    found_next = True
                    break

            if not found_next:
                # Если путь зашел в тупик, откатываем назад
                grid[path[-1][0]][path[-1][1]] = 0
                path.pop()

        path_id += 1

    return grid

def assign_start_end_points(grid, K):
    """Назначает стартовые и конечные точки для каждого пути."""
    start_points = []
    end_points = []

    for path_id in range(1, K + 1):
        cells = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == path_id]
        start_points.append(cells[0])
        end_points.append(cells[-1])

    return start_points, end_points

def print_grid(grid):
    """Печатает матрицу."""
    for row in grid:
        print(" ".join(str(x) if x > 0 else '.' for x in row))

# Пример использования
M, N = 7, 7  # Размер матрицы
K = 5  # Количество путей

grid = generate_random_paths(M, N, K)
start_points, end_points = assign_start_end_points(grid, K)

print("Сгенерированная матрица:")
print_grid(grid)

print("\nСтартовые точки:", start_points)
print("Конечные точки:", end_points)
