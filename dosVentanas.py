import tkinter as tk
import random

class Tetris:
    def __init__(self, master):
        self.master = master
        self.master.title("Tetris")
        self.master.resizable(False, False)

        self.WIDTH = 300
        self.HEIGHT = 600
        self.BLOCK_SIZE = 30
        self.COLS = self.WIDTH // self.BLOCK_SIZE
        self.ROWS = self.HEIGHT // self.BLOCK_SIZE
        
        self.canvas = tk.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()
        
        # Center window
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.WIDTH) // 2
        y = (screen_height - self.HEIGHT) // 2
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

        self.shapes = [
            [[1, 1, 1, 1]], # I
            [[1, 1], [1, 1]], # O
            [[1, 1, 1], [0, 1, 0]], # T
            [[1, 1, 1], [1, 0, 0]], # L
            [[1, 1, 1], [0, 0, 1]], # J
            [[1, 1, 0], [0, 1, 1]], # Z
            [[0, 1, 1], [1, 1, 0]]  # S
        ]
        
        self.colors = ["cyan", "yellow", "purple", "orange", "blue", "red", "green"]
        
        self.grid = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.score = 0
        self.game_over = False
        
        self.current_piece = self.new_piece()
        self.draw_grid()
        
        self.master.bind("<Left>", lambda e: self.move(-1, 0))
        self.master.bind("<Right>", lambda e: self.move(1, 0))
        self.master.bind("<Down>", lambda e: self.move(0, 1))
        self.master.bind("<Up>", lambda e: self.rotate())
        
        self.run_game()

    def new_piece(self):
        shape = random.choice(self.shapes)
        color = self.colors[self.shapes.index(shape)]
        return {
            "shape": shape,
            "color": color,
            "x": self.COLS // 2 - len(shape[0]) // 2,
            "y": 0
        }

    def draw_grid(self):
        self.canvas.delete("all")
        # Draw static blocks
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.grid[r][c]:
                    x1 = c * self.BLOCK_SIZE
                    y1 = r * self.BLOCK_SIZE
                    x2 = x1 + self.BLOCK_SIZE
                    y2 = y1 + self.BLOCK_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.grid[r][c], outline="white")

        # Draw current piece
        if self.current_piece:
            for r, row in enumerate(self.current_piece["shape"]):
                for c, val in enumerate(row):
                    if val:
                        x1 = (self.current_piece["x"] + c) * self.BLOCK_SIZE
                        y1 = (self.current_piece["y"] + r) * self.BLOCK_SIZE
                        x2 = x1 + self.BLOCK_SIZE
                        y2 = y1 + self.BLOCK_SIZE
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.current_piece["color"], outline="white")
        
        # Draw Score
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 14), anchor="w")
        
        if self.game_over:
            self.canvas.create_text(self.WIDTH//2, self.HEIGHT//2, text="GAME OVER", fill="red", font=("Arial", 30))

    def move(self, dx, dy):
        if self.game_over: return
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece["x"] += dx
            self.current_piece["y"] += dy
            self.draw_grid()
            return True
        elif dy > 0: # Hit bottom or another piece while moving down
            self.lock_piece()
            return False
        return False

    def rotate(self):
        if self.game_over: return
        shape = self.current_piece["shape"]
        new_shape = [list(row) for row in zip(*shape[::-1])]
        if not self.check_collision({"shape": new_shape, "x": self.current_piece["x"], "y": self.current_piece["y"]}, 0, 0):
            self.current_piece["shape"] = new_shape
            self.draw_grid()

    def check_collision(self, piece, dx, dy):
        for r, row in enumerate(piece["shape"]):
            for c, val in enumerate(row):
                if val:
                    new_x = piece["x"] + c + dx
                    new_y = piece["y"] + r + dy
                    if new_x < 0 or new_x >= self.COLS or new_y >= self.ROWS:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def lock_piece(self):
        for r, row in enumerate(self.current_piece["shape"]):
            for c, val in enumerate(row):
                if val:
                    self.grid[self.current_piece["y"] + r][self.current_piece["x"] + c] = self.current_piece["color"]
        
        self.clear_lines()
        self.current_piece = self.new_piece()
        if self.check_collision(self.current_piece, 0, 0):
            self.game_over = True
        self.draw_grid()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(x is None for x in row)]
        lines_cleared = self.ROWS - len(new_grid)
        if lines_cleared > 0:
            self.score += lines_cleared * 100
            for _ in range(lines_cleared):
                new_grid.insert(0, [None for _ in range(self.COLS)])
            self.grid = new_grid

    def run_game(self):
        if not self.game_over:
            self.move(0, 1)
            self.master.after(500, self.run_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = Tetris(root)
    root.mainloop()
