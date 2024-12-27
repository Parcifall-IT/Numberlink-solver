import tkinter as tk
from tkinter import messagebox
from sat import solve_puzzle
import random


class NumberlinkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Numberlink Game")
        self.root.geometry("500x500")
        self.root.configure(bg="#f7f7f7")

        self.rows = 0
        self.cols = 0
        self.grid = []
        self.entries = []
        self.canvas = None
        self.colors = []

        self.start_screen()

    def bind_enter_to_button(self, button):
        """Привязывает нажатие Enter к переданной кнопке."""
        self.root.bind("<Return>", lambda event: button.invoke())

    def bind_arrows_to_entries(self):
        """Привязывает переключение между полями ввода с помощью стрелок."""
        for i, row in enumerate(self.entries):
            for j, entry in enumerate(row):
                entry.bind("<Up>", lambda event, x=i, y=j: self.focus_entry(x - 1, y))
                entry.bind("<Down>", lambda event, x=i, y=j: self.focus_entry(x + 1, y))
                entry.bind("<Left>", lambda event, x=i, y=j: self.focus_entry(x, y - 1))
                entry.bind("<Right>", lambda event, x=i, y=j: self.focus_entry(x, y + 1))
        self.focus_entry(0, 0)

    def focus_entry(self, x, y):
        """Устанавливает фокус на указанное поле ввода, если оно существует."""
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.entries[x][y].focus()

    @staticmethod
    def generate_random_colors(n):
        colors = set()
        while len(colors) < n:
            color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
            colors.add(color)
        return list(colors)

    def start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Добро пожаловать в Numberlink!",
            font=("Arial", 16, "bold"),
            bg="#f7f7f7",
        ).pack(pady=20)

        input_frame = tk.Frame(self.root, bg="#f7f7f7")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Длина (строки):", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, padx=5)
        self.rows_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
        self.rows_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Ширина (столбцы):", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, padx=5)
        self.cols_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
        self.cols_entry.grid(row=1, column=1, padx=5)

        create_button = tk.Button(
            self.root,
            text="Создать поле",
            command=self.create_grid,
            font=("Arial", 12),
            bg="#4caf50",
            fg="white",
            activebackground="#45a049",
            relief="raised",
        )
        create_button.pack(pady=20)

        self.rows_entry.bind("<Down>", lambda event: self.cols_entry.focus())
        self.cols_entry.bind("<Up>", lambda event: self.rows_entry.focus())
        self.rows_entry.focus()
        self.bind_enter_to_button(create_button)  # Привязать Enter к кнопке

    def create_grid(self):
        try:
            self.rows = int(self.rows_entry.get())
            self.cols = int(self.cols_entry.get())
            if self.rows <= 0 or self.cols <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные размеры поля!")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.entries = []

        grid_frame = tk.Frame(self.root, bg="#f7f7f7")
        grid_frame.pack(pady=20)

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                entry = tk.Entry(grid_frame, width=3, justify="center", font=("Arial", 12))
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.entries.append(row)

        self.bind_arrows_to_entries()

        solve_button = tk.Button(
            self.root,
            text="Решить",
            command=self.solve,
            font=("Arial", 12),
            bg="#2196f3",
            fg="white",
            activebackground="#1e88e5",
            relief="raised",
        )
        solve_button.pack(pady=10)

        self.bind_enter_to_button(solve_button)  # Привязать Enter к кнопке

    def solve(self):
        try:
            for i in range(self.rows):
                for j in range(self.cols):
                    value = self.entries[i][j].get()
                    self.grid[i][j] = int(value) if value else 0
        except ValueError:
            messagebox.showerror("Ошибка", "Все поля должны содержать числа или быть пустыми!")
            return

        result = solve_puzzle(self.grid)
        if result == "Задача не имеет решения":
            self.show_no_solution()
        else:
            self.show_solution(result)

    def show_no_solution(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Решение не найдено!",
            font=("Arial", 16, "bold"),
            fg="red",
            bg="#f7f7f7",
        ).pack(pady=20)

        return_button = tk.Button(
            self.root,
            text="Вернуться к вводу",
            command=self.start_screen,
            font=("Arial", 12),
            bg="#2196f3",
            fg="white",
            activebackground="#1e88e5",
            relief="raised",
        )
        return_button.pack(pady=20)

        self.bind_enter_to_button(return_button)  # Привязать Enter к кнопке

    def show_solution(self, result):
        self.colors = self.generate_random_colors(len(result))

        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.root, width=self.cols * 40, height=self.rows * 40, bg="white")
        self.canvas.pack(pady=10)

        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * 40, i * 40
                x1, y1 = x0 + 40, y0 + 40
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

                if self.grid[i][j] > 0:
                    self.canvas.create_text(
                        x0 + 20, y0 + 20, text=str(self.grid[i][j]), font=("Arial", 14, "bold"), fill="#333333"
                    )
                elif self.grid[i][j] == -1:  # Отображаем стенки
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")

        color_map = {}
        for num, points in result:
            if num not in color_map:
                color_map[num] = self.colors[(num - 1) % len(self.colors)]
            color = color_map[num]

            ordered_points = order_path(points)

            for i in range(len(ordered_points) - 1):
                x0, y0 = ordered_points[i][1] * 40 + 20, ordered_points[i][0] * 40 + 20
                x1, y1 = ordered_points[i + 1][1] * 40 + 20, ordered_points[i + 1][0] * 40 + 20
                self.canvas.create_line(x0, y0, x1, y1, fill=color, width=3)

        return_button = tk.Button(
            self.root,
            text="Вернуться к вводу",
            command=self.start_screen,
            font=("Arial", 12),
            bg="#2196f3",
            fg="white",
            activebackground="#1e88e5",
            relief="raised",
        )
        return_button.pack(pady=20)

        self.bind_enter_to_button(return_button)  # Привязать Enter к кнопке


def order_path(points):
    from collections import defaultdict

    adjacency = defaultdict(list)
    for x, y in points:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if neighbor in points:
                adjacency[(x, y)].append(neighbor)

    start = None
    for point, neighbors in adjacency.items():
        if len(neighbors) == 1:
            start = point
            break

    if not start:
        raise ValueError("Не удалось определить начальную точку пути")

    ordered_path = []
    current = start
    visited = set()

    while current and current not in visited:
        ordered_path.append(current)
        visited.add(current)
        neighbors = [n for n in adjacency[current] if n not in visited]
        current = neighbors[0] if neighbors else None

    return ordered_path


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberlinkApp(root)
    root.mainloop()
