import tkinter as tk
from tkinter.simpledialog import askstring


def get_player_name():
    root = tk.Tk()
    # root.iconbitmap("../assets/img/ui/retro_icon.ico")
    root.withdraw()  # Hide the main window
    player_name = askstring("High Score", "Enter your name:")

    return player_name


# Example usage:
player_name = get_player_name()
print("Entered Name:", player_name)
