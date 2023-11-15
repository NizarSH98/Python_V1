import tkinter as tk
from tkinter import messagebox
import heapq

class PuzzleState:
    def __init__(self, puzzle, moves=0):
        self.puzzle = puzzle
        self.moves = moves

    def __lt__(self, other):
        return self.moves < other.moves

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def __hash__(self):
        return hash(tuple(map(tuple, self.puzzle)))

def get_empty_position(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                return (i, j)

def get_possible_moves(puzzle):
    i, j = get_empty_position(puzzle)
    possible_moves = []

    if i > 0:
        possible_moves.append((i-1, j))  # Move block above empty space
    if i < 2:
        possible_moves.append((i+1, j))  # Move block below empty space
    if j > 0:
        possible_moves.append((i, j-1))  # Move block to the left of empty space
    if j < 2:
        possible_moves.append((i, j+1))  # Move block to the right of empty space

    return possible_moves

def swap_positions(puzzle, pos1, pos2):
    new_puzzle = [row[:] for row in puzzle]
    new_puzzle[pos1[0]][pos1[1]], new_puzzle[pos2[0]][pos2[1]] = new_puzzle[pos2[0]][pos2[1]], new_puzzle[pos1[0]][pos1[1]]
    return new_puzzle

def h(puzzle, target):
    return sum([1 for i in range(3) for j in range(3) if puzzle[i][j] != target[i][j]])

def a_star(initial_state, target_state):
    open_list = []
    heapq.heappush(open_list, (0, initial_state))
    closed_set = set()

    while open_list:
        _, current_state = heapq.heappop(open_list)

        if current_state.puzzle == target_state.puzzle:
            return current_state.moves

        closed_set.add(current_state)

        for move in get_possible_moves(current_state.puzzle):
            new_puzzle = swap_positions(current_state.puzzle, get_empty_position(current_state.puzzle), move)
            new_state = PuzzleState(new_puzzle, current_state.moves + 1)

            if new_state not in closed_set:
                priority = new_state.moves + h(new_state.puzzle, target_state.puzzle)
                heapq.heappush(open_list, (priority, new_state))

class PuzzleGUI:
    def __init__(self, master, initial_puzzle, target_puzzle):
        self.master = master
        self.master.title("Arrange Puzzle Solver")

        self.canvas = tk.Canvas(self.master, width=300, height=300)
        self.canvas.pack()

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart)
        self.restart_button.pack()

        self.solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        self.solve_button.pack()

        self.puzzle = initial_puzzle
        self.target_puzzle = target_puzzle
        self.draw_puzzle()
        self.move_queue = []

    def draw_puzzle(self):
        self.canvas.delete("all")
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] != 0:
                    self.canvas.create_rectangle(j * 100, i * 100, (j + 1) * 100, (i + 1) * 100, fill="lightblue")
                    self.canvas.create_text(j * 100 + 50, i * 100 + 50, text=str(self.puzzle[i][j]), font=("Helvetica", 24, "bold"))

    def restart(self):
        self.puzzle = initial_puzzle
        self.draw_puzzle()

    def solve(self):
        initial_state = PuzzleState(self.puzzle)
        target_state = PuzzleState(self.target_puzzle)

        open_list = []
        heapq.heappush(open_list, (0, initial_state))
        closed_set = set()

        def do_solve():
            if open_list:
                _, current_state = heapq.heappop(open_list)

                if current_state.puzzle == target_state.puzzle:
                    messagebox.showinfo("Solution", f"Number of moves needed: {current_state.moves}")
                    return

                closed_set.add(current_state)

                for move in get_possible_moves(current_state.puzzle):
                    new_puzzle = swap_positions(current_state.puzzle, get_empty_position(current_state.puzzle), move)
                    new_state = PuzzleState(new_puzzle, current_state.moves + 1)

                    if new_state not in closed_set:
                        priority = new_state.moves + h(new_state.puzzle, target_state.puzzle)
                        heapq.heappush(open_list, (priority, new_state))

                self.puzzle = current_state.puzzle
                self.draw_puzzle()

                self.master.after(250, do_solve)  # Schedule the next step

            else:
                messagebox.showinfo("No Solution", "No solution found.")

        do_solve()
    

if __name__ == "__main__":
    initial_puzzle = [[1, 8, 5], [4, 3, 6], [7, 2, 0]]
    target_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    root = tk.Tk()
    gui = PuzzleGUI(root, initial_puzzle, target_puzzle)
    root.mainloop()
