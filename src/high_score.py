import os.path
import sqlite3
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox


class HighScoreManager:
    """Manages a high-score database"""
    def __init__(self):
        self.con = sqlite3.connect("scores_db/scores.db")
        self.cur = self.con.cursor()
        self.root = tk.Tk()

    def create_db(self):
        if not os.path.exists("scores_db/scores.db"):
            with open("scores_db/scores.sql", 'r', encoding='utf-8') as sql_file:
                try:
                    self.cur.executescript(sql_file.read())
                    self.con.commit()
                    print("Database created")
                except sqlite3.Error as e:
                    print(f"sqlite error: {e}")
        else:
            print("Database exists, proceeding...")

    def close_db(self):
        self.con.close()

    def retrieve_all_scores(self):
        query = "SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 10"
        self.cur.execute(query)
        return self.cur.fetchall()

    def check_high_score(self, player_score):
        top_10 = self.retrieve_all_scores()
        if len(top_10) < 10 or player_score > top_10[-1][1]:
            player_name = self.get_player_name()
            if player_name is not None:
                self.save_score(player_name, player_score)
            else:
                messagebox.showerror("Error", "Please enter your name")

    def save_score(self, player_name, score):
        query = "INSERT INTO scores (player_name, score) VALUES (?, ?)"
        self.cur.execute(query, (player_name, score))
        self.con.commit()
        self.remove_lowest_score()

    def remove_lowest_score(self):
        query = "DELETE FROM scores WHERE id NOT IN (SELECT id FROM scores ORDER BY score DESC LIMIT 10)"
        self.cur.execute(query)
        self.con.commit()

    def get_player_name(self):
        self.root.withdraw()
        player_name = askstring("High Score", "Enter your name:")
        return player_name

    def insert_10_sample_records(self):
        name = "paichiwo"
        for i in range(1, 11):
            score = i * 100
            self.save_score(name, score)
