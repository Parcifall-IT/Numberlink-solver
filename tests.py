import unittest
from main import solve_puzzle


class TestPuzzleSolver(unittest.TestCase):
    def test_simple_case(self):
        matrix = [
            [1, 0, 1],
            [2, 0, 2],
            [3, 0, 3]
        ]
        expected = [
            (1, {(0, 0), (0, 1), (0, 2)}),
            (2, {(1, 0), (1, 1), (1, 2)}),
            (3, {(2, 0), (2, 1), (2, 2)})
        ]
        solution = solve_puzzle(matrix)
        self.assertEqual(solution, expected)

    def test_hard_case(self):
        matrix = [
            [0, 0, 0, 4, 0, 0, 0],
            [0, 3, 0, 0, 2, 5, 0],
            [0, 0, 0, 3, 1, 0, 0],
            [0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [2, 0, 0, 0, 4, 0, 0]
        ]
        expected = [
            (1, {(2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (5, 2)}),
            (2, {(1, 4), (1, 3), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}),
            (3, {(1, 1), (2, 1), (2, 2), (2, 3)}),
            (4, {(0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (6, 4)}),
            (5, {(1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (6, 3), (6, 2), (6, 1), (5, 1), (4, 1), (3, 1), (3, 2), (3, 3)})
        ]
        solution = solve_puzzle(matrix)
        self.assertEqual(solution, expected)

    def test_no_path(self):
        matrix = [
            [1, 2],
            [2, 1]
        ]
        expected = "Задача не имеет решения"
        solution = solve_puzzle(matrix)
        self.assertEqual(solution, expected)


if __name__ == '__main__':
    unittest.main()
