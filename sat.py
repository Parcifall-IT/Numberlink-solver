from z3 import Solver, Sum, Int, If, And, Or, sat


def solveEm(board, M, N):
    B = [[Int(f'B_{i}_{j}') for j in range(N)] for i in range(M)]

    s = Solver()

    # Ограничения: фиксированные клетки и стенки
    s.add([
        If(board[i][j] > 0, B[i][j] == board[i][j],
           If(board[i][j] == -1, B[i][j] == -1, And(B[i][j] >= 1, B[i][j] < 100)))
        for i in range(M) for j in range(N)
    ])

    # Ограничения на соседей: у фиксированных клеток ровно один сосед того же цвета
    for i in range(M):
        for j in range(N):
            if board[i][j] != -1:  # Игнорируем стенки
                same_neighs_ij = Sum([
                    If(B[i][j] == B[k][l], 1, 0)
                    for k, l in neighbors(i, j, M, N) if board[k][l] != -1
                ])
                if board[i][j] > 0:
                    s.add(same_neighs_ij == 1)
                else:
                    s.add(Or(same_neighs_ij == 2, B[i][j] == 0))

    if s.check() == sat:
        m = s.model()
        return [[m[B[i][j]].as_long() for j in range(N)] for i in range(M)]
    return None


def neighbors(i, j, M, N):
    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < M and 0 <= nj < N:
            yield ni, nj


def findSrcandDest(matrix):
    coordinates = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            color = matrix[i][j]
            if color != 0:
                if color not in coordinates:
                    coordinates[color] = {'src': (i, j), 'dest': None}
                else:
                    coordinates[color]['dest'] = (i, j)
    return coordinates


def dfs(matrix, visited, current, target, path, all_paths, color):
    i, j = current
    visited[i][j] = True
    path.append(current)

    if current == target:
        all_paths.append(path.copy())
    else:
        for ni, nj in neighbors(i, j, len(matrix), len(matrix[0])):
            if not visited[ni][nj] and matrix[ni][nj] == color:
                dfs(matrix, visited, (ni, nj), target, path, all_paths, color)

    path.pop()
    visited[i][j] = False


def extractPaths(matrix, coordinates):
    paths = {}
    for color, coords in coordinates.items():
        src, dest = coords['src'], coords['dest']
        visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
        path, all_paths = [], []
        dfs(matrix, visited, src, dest, path, all_paths, color)
        if all_paths:
            paths[color] = all_paths[0]
    return paths


def solve_puzzle(matrix):
    M, N = len(matrix), len(matrix[0])
    solved_matrix = solveEm(matrix, M, N)
    if not solved_matrix:
        return 'Задача не имеет решения'

    coordinates = findSrcandDest(matrix)
    paths = extractPaths(solved_matrix, coordinates)
    return sorted([(color, set(path)) for color, path in paths.items()], key=lambda x: x[0])


def main():
    matrix = [
        [1, 0, 0],
        [2, 2, 0],
        [1, 0, 0]
    ]
    print(solve_puzzle(matrix))


if __name__ == "__main__":
    main()
