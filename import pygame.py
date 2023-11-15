import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_SIZE = 600
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Define fonts
FONT = pygame.font.Font(None, 36)

# Define the Sudoku grid (9x9)
GRID_SIZE = 9
GRID_WIDTH = WINDOW_SIZE // GRID_SIZE

# Define a sample Sudoku puzzle (replace this with your generator later)


def draw_grid(selected_row, selected_col):
    for i in range(GRID_SIZE + 1):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(WINDOW, BLACK, (i * GRID_WIDTH, 0), (i * GRID_WIDTH, WINDOW_SIZE), thickness)
        pygame.draw.line(WINDOW, BLACK, (0, i * GRID_WIDTH), (WINDOW_SIZE, i * GRID_WIDTH), thickness)

    # Draw the selected cell
    if selected_row is not None and selected_col is not None:
        pygame.draw.rect(WINDOW, BLUE, (selected_col * GRID_WIDTH, selected_row * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH), 5)


def draw_numbers(puzzle, selected_row, selected_col):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if puzzle[i][j] != 0:
                text = FONT.render(str(puzzle[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * GRID_WIDTH + GRID_WIDTH/2, i * GRID_WIDTH + GRID_WIDTH/2))
                WINDOW.blit(text, text_rect)

    if selected_row is not None and selected_col is not None:
        pygame.draw.rect(WINDOW, BLUE, (selected_col * GRID_WIDTH, selected_row * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH), 5)


def draw_mask(row, col):
    mask = pygame.Surface((GRID_WIDTH, GRID_WIDTH), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 128))  # Semi-transparent black
    WINDOW.blit(mask, (col * GRID_WIDTH, row * GRID_WIDTH))




def draw_selected_cell(row, col):
    overlay = pygame.Surface((GRID_WIDTH, GRID_WIDTH), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 255, 128), (0, 0, GRID_WIDTH, GRID_WIDTH), 5)
    WINDOW.blit(overlay, (col * GRID_WIDTH, row * GRID_WIDTH))





def generate_valid_sudoku():
    def is_valid(board, row, col, num):
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False

        # Check 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def solve(board):
        empty_cell = find_empty_cell(board)
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                if solve(board):
                    return True
                board[row][col] = 0

        return False

    def find_empty_cell(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    # Initialize an empty Sudoku grid
    sudoku_board = [[0 for _ in range(9)] for _ in range(9)]

    # Generate a random completed Sudoku puzzle
    solve(sudoku_board)

    # Create a copy of the completed puzzle
    puzzle = [row[:] for row in sudoku_board]

    # Remove numbers to create a playable puzzle
    num_removed = 45  # Adjust this number to control puzzle difficulty
    for _ in range(num_removed):
        row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = 0

    return puzzle


def is_solved(puzzle):
    def is_valid(board, row, col, num):
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False

        # Check 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return False

            num = puzzle[i][j]
            puzzle[i][j] = 0

            if not is_valid(puzzle, i, j, num):
                return False

            puzzle[i][j] = num

    return True


def main():
    PUZZLE = generate_valid_sudoku()  # Generate a new Sudoku puzzle

    selected_row, selected_col = None, None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected_row = y // GRID_WIDTH
                selected_col = x // GRID_WIDTH

            if event.type == pygame.KEYDOWN:
                if selected_row is not None and selected_col is not None:
                    if PUZZLE[selected_row][selected_col] == 0:  # Check if the cell is empty
                        if event.unicode.isdigit() and int(event.unicode) in range(1, 10):
                            PUZZLE[selected_row][selected_col] = int(event.unicode)
                            
                        if is_solved(PUZZLE):
                            print("Congratulations! You've solved the puzzle.")

        WINDOW.fill(WHITE)
        draw_grid(selected_row, selected_col)
        draw_numbers(PUZZLE, selected_row, selected_col)

        pygame.display.flip()

if __name__ == "__main__":
    main()


