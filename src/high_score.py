import os
import sqlite3
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox


class HighScoreManager:
    """Manages a high-score database"""
    def __init__(self):
        self.cur = None
        self.con = None
        self.db_path = "scores_db/scores.db"
        self.sql_script_path = "scores_db/scores.sql"
        self.root = tk.Tk()
        self.ensure_db()

    def ensure_db(self):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Connect to the database
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()

        # Check if the table exists, if not, create it
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scores'")
        if not self.cur.fetchone():
            self.create_db()
            self.insert_10_sample_records()

    def create_db(self):
        with open(self.sql_script_path, 'r', encoding='utf-8') as sql_file:
            try:
                self.cur.executescript(sql_file.read())
                self.con.commit()
                print("Database created")
            except sqlite3.Error as e:
                print(f"SQLite error: {e}")

    def close_db(self):
        if self.con:
            self.con.close()

    def retrieve_all_scores(self):
        query = "SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 10"
        self.cur.execute(query)
        return self.cur.fetchall()

    def check_high_score(self, player_score):
        top_10 = self.retrieve_all_scores()
        if len(top_10) < 10 or player_score > top_10[-1][1]:
            player_name = self.get_player_name()
            if player_name:
                self.save_score(player_name, player_score)
            else:
                messagebox.showerror("Error", "Please enter your name")

    def save_score(self, player_name, score):
        query = "INSERT INTO scores (player_name, score) VALUES (?, ?)"
        self.cur.execute(query, (player_name, score))
        self.con.commit()
        # self.remove_lowest_score()

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

