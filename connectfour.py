"""Arnav Patel's version of a tic-tac-toe based Connect 4 game built using Python and Tkinter."""

# For tutorial help, go to this link: https://realpython.com/tic-tac-toe-python/

import tkinter as tk
#print(tk.TkVersion)
from tkinter import font

# If your tkinter version is less than 8.6, you need to either download python package or install a more recent version of python.
# Then, change your interpreter to that updated version, so the print statement returns at least 8.6.

class GameBoard(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Connect 4")
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

        for row in range(6):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)

            for col in range(7):
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
    
def main():
    board = GameBoard()
    board.mainloop()
    
if __name__ == "__main__":
    main()






        
