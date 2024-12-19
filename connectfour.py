"""Arnav Patel's version of a tic-tac-toe game built using Python and Tkinter."""

# For tutorial help, go to this link: https://realpython.com/tic-tac-toe-python/

import tkinter as tk
#print(tk.TkVersion)
from tkinter import font
from typing import NamedTuple
from itertools import cycle

# If your tkinter version is less than 8.6, you need to either download python package or install a more recent version of python.
# Then, change your interpreter to that updated version, so the print statement returns at least 8.6.

class Player(NamedTuple):
    label: str
    color: str



class Move(NamedTuple):
    row: int
    col: int
    label: str = ""



BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label = "X", color = "blue"),
    Player(label = "O", color = "red"),
)


class GameBoard(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe!")
        self.cells = {}

        self.create_board_display()
        self.create_board_grid()
    
    def create_board_display(self):
        display_frame = tk.Frame(master = self)
        display_frame.pack(fill = tk.X)
        self.display = tk.Label(
            master = display_frame,
            text = "Ready to Play?",
            font = font.Font(size = 30, weight = "bold"),
        )
        self.display.pack()
    
    def create_board_grid(self):
        grid_frame = tk.Frame(master = self)
        grid_frame.pack()

        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)

            for col in range(3):
                button = tk.Button(
                        master = grid_frame,
                        text = "",
                        font = font.Font(size=38, weight="bold"),
                        fg= "black",
                        width=3,
                        height=2,
                        highlightbackground= "lightgreen",
                    )
                self.cells[button] = (row, col)

                button.grid(
                        row = row,
                        column = col,
                        padx = 5,
                        pady = 5,
                        stick = "nsew"
                    )


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self.player = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.player)
        self.winner_combo = []
        self.current_moves = []
        self.has_winner = False
        self.winning_combos = []
        self.setup_board()

    def setup_board(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self.winning_combos = self.get_winning_combos()

    def get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self.current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]


def main():
    board = GameBoard()
    board.mainloop()
    
if __name__ == "__main__":
    main()




        
