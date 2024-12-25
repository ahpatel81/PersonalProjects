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
    def __init__(self, players = DEFAULT_PLAYERS, board_size = BOARD_SIZE):
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
    
    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self.current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self.current_moves[row][col] = move
        for combo in self.winning_combos:
            results = set(
                self.current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    
    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner
    
    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self.current_moves for move in row
        )
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self.players)


def main():
    board = GameBoard()
    board.mainloop()
    
if __name__ == "__main__":
    main()




        
