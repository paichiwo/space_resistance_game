import os
import csv
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox


class HighScoreManager:
    """Manages a high-score database stored in a text file."""
    def __init__(self):
        self.file_path = "data/scores.txt"
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window initially
        self.ensure_file()

    def ensure_file(self):
        """Ensures that the text file exists."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["player_name", "score"])  # Write the header
                self.insert_sample_records(writer)

    def retrieve_all_scores(self):
        """Retrieves the top 10 high scores from the text file."""
        scores = []
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                scores.append((row["player_name"], int(row["score"])))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:10]

    def check_high_score(self, player_score):
        """Checks if the given score is a high score and, if so, saves it."""
        top_10 = self.retrieve_all_scores()
        if len(top_10) < 10 or player_score > top_10[-1][1]:
            player_name = self.get_player_name()
            if player_name:
                self.save_score(player_name, player_score)
            else:
                messagebox.showerror("Error", "Please enter your name")

    def save_score(self, player_name, score):
        """Saves a new high score to the text file."""
        scores = self.retrieve_all_scores()
        scores.append((player_name, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:10]  # Keep only the top 10 scores

        with open(self.file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["player_name", "score"])  # Write the header
            for player, score in scores:
                writer.writerow([player, score])

    @staticmethod
    def get_player_name():
        """Prompts the player to enter their name."""
        return askstring("High Score", "Enter your name:")

    @staticmethod
    def insert_sample_records(writer):
        """Inserts 10 sample records into the text file."""
        name = "paichiwo"
        for i in range(1, 11):
            score = i * 100
            writer.writerow([name, score])