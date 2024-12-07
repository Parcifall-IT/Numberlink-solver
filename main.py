from collections import deque

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


def bfs(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and (matrix[x][y] == 0 or (x, y) == end)

    queue = deque([([start], start)])
    all_paths = []

    while queue:
        path, (x, y) = queue.popleft()

        if (x, y) == end:
            all_paths.append(path)
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and (nx, ny) not in path:
                queue.append((path + [(nx, ny)], (nx, ny)))

    return all_paths


def find_all_paths(matrix, numbers):
    all_paths = {}
    for num, positions in numbers.items():
        if len(positions) == 2:
            start, end = positions
            paths = bfs(matrix, start, end)
            if paths:
                all_paths[num] = paths
            else:
                all_paths[num] = []
    return all_paths


def paths_intersect(path1, path2):
    return bool(set(path1) & set(path2))


def solve(matrix, numbers, all_paths, current_num, current_paths, used_paths):
    if current_num > max(numbers.keys()):
        return current_paths

    if current_num not in all_paths or not all_paths[current_num]:
        return None
    for path in all_paths[current_num]:
        if any(paths_intersect(path, used_path) for used_path in used_paths):
            continue

        new_used_paths = used_paths + [path]
        new_current_paths = current_paths + [(current_num, path)]

        result = solve(matrix, numbers, all_paths, current_num + 1, new_current_paths, new_used_paths)
        if result:
            return result

    return None


def solve_puzzle(matrix):
    numbers = find_numbers(matrix)
    all_paths = find_all_paths(matrix, numbers)

    solution = solve(matrix, numbers, all_paths, 1, [], [])
    return solution if solution else "Задача не имеет решения"


if __name__ == '__main__':
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
