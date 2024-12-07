from collections import deque
from joblib import Parallel, delayed, cpu_count
from functools import lru_cache

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_numbers(matrix):
    numbers = {}
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val != 0:
                if val not in numbers:
                    numbers[val] = []
                numbers[val].append((i, j))
    return numbers


def bfs_all_paths(matrix, start, end, max_paths=500):
    rows, cols = len(matrix), len(matrix[0])

    def is_valid(x, y, visited):
        return 0 <= x < rows and 0 <= y < cols and (matrix[x][y] == 0 or (x, y) == end) and (x, y) not in visited

    queue = deque([({start}, start)])
    all_paths = []

    while queue and len(all_paths) < max_paths:
        path, (x, y) = queue.popleft()

        if (x, y) == end:
            all_paths.append(path)
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, set(path)):
                queue.append((path | {(nx, ny)}, (nx, ny)))

    return all_paths


def process_number(matrix, positions):
    start, end = positions
    return bfs_all_paths(matrix, start, end)


def find_all_paths(matrix, numbers):
    all_paths = {}
    n_jobs = min(cpu_count(), len(numbers))
    results = Parallel(n_jobs=n_jobs)(delayed(process_number)(matrix, positions)
                                  for num, positions in numbers.items())
    for (num, positions), paths in zip(numbers.items(), results):
        all_paths[num] = paths
    return all_paths


def solve(matrix, numbers, all_paths, current_num, current_paths, used_cells):
    if current_num > max(numbers.keys()):
        return current_paths

    if current_num not in all_paths or not all_paths[current_num]:
        return None

    for path in all_paths[current_num]:
        if any(cell in used_cells for cell in path):
            continue

        new_used_cells = used_cells | path
        new_current_paths = current_paths + [(current_num, path)]

        result = solve(matrix, numbers, all_paths, current_num + 1, new_current_paths, new_used_cells)
        if result:
            return result

    return None


def solve_puzzle(matrix):
    numbers = find_numbers(matrix)

    all_paths = find_all_paths(matrix, numbers)

    solution = solve(matrix, numbers, all_paths, 1, [], set())
    return solution if solution else "Задача не имеет решения"


def main():
    matrix = [
        [0, 0, 0, 4, 0, 0, 0],
        [0, 3, 0, 0, 2, 5, 0],
        [0, 0, 0, 3, 1, 0, 0],
        [0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [2, 0, 0, 0, 4, 0, 0]
    ]

    solution = solve_puzzle(matrix)
    print(solution)


if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    main()
    finish = datetime.datetime.now()
    print(finish - start)
