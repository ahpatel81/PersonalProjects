"""Arnav Patel's version of a tic-tac-toe game built using Python and Tkinter."""

# For tutorial help, go to this link: https://realpython.com/tic-tac-toe-python/

import tkinter as tk
#print(tk.TkVersion)
from tkinter import font

# If your tkinter version is less than 8.6, you need to either download python package or install a more recent version of python.
# Then, change your interpreter to that updated version, so the print statement returns at least 8.6.

class GameBoard(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Xs and Os")
        self.cells = {}
