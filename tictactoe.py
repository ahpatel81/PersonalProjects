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
    Player(label = "O", color = "green"),
)


class GameBoard(tk.Tk):

    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe!")
        self.cells = {}

        self.oWins = 0
        self.xWins = 0

        self._game = game
        self._create_menu()

        self.create_board_display()
        self.create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)


    def update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)
    
    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self.update_display(msg="Ready?")
        for button in self.cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

    def update_display(self, msg, color="white"):
        self.display["text"] = msg
        self.display["fg"] = color
    
    def _highlight_cells(self):
        for button, coordinates in self.cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")
    
    def create_board_display(self):
        display_frame = tk.Frame(master = self)
        display_frame.pack(fill = tk.X)
        self.display = tk.Label(
            master = display_frame,
            text = f"X Wins: {self.xWins}    Ready to Play?    O Wins: {self.oWins}",
            font = font.Font(size = 30, weight = "bold"),
        )
        self.display.pack()
    
    def create_board_grid(self):
        grid_frame = tk.Frame(master = self)
        grid_frame.pack()

        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)

            for col in range(self._game.board_size):
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
                button.bind("<ButtonPress-1>", self.play)

                button.grid( row = row, column = col, padx = 5, pady = 5, sticky = "nsew")
    
    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self.cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self.update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self.update_display(msg="Tied game!", color="yellow")
            elif self._game.has_winner():
                self._highlight_cells()

                if self._game.current_player.label == 'X':
                    self.xWins += 1
                elif self._game.current_player.label == 'O':
                    self.oWins += 1

                msg = f'X Wins: {self.xWins}    Player "{self._game.current_player.label}" wins!    O Wins: {self.oWins}'
                color = self._game.current_player.color
                self.update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"X Wins: {self.xWins}    {self._game.current_player.label}'s turn    O Wins: {self.oWins}"
                self.update_display(msg)


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self.setup_board()
    
    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

    def setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self.get_winning_combos()

    def get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
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
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)


def main():
    game = TicTacToeGame()
    board = GameBoard(game)
    board.mainloop()
    
if __name__ == "__main__":
    main()

