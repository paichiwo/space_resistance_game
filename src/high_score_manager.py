import os
import json


class HighScoreManager:
    def __init__(self):
        super().__init__()
        self.file_path = 'data/scores.json'
        self.create_scores_file()

    def create_scores_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({'scores': []}, file, indent=4)
            self.insert_sample_records()

    def retrieve_all_scores(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            scores = [(entry['player_name'], entry['score']) for entry in data['scores']]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:10]

    def retrieve_lowest_score(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            lowest_score = min(data['scores'], key=lambda x: x['score'])
            return lowest_score['score']

    def check_high_score(self, player_score):
        top_10 = self.retrieve_all_scores()
        return True if len(top_10) < 10 or player_score > top_10[-1][1] else False

    def save_score(self, player_name, score):
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        data['scores'].append({'player_name': player_name, 'score': score})
        data['scores'].sort(key=lambda x: x['score'], reverse=True)
        data['scores'] = data['scores'][:10]  # Keep only the top 10 scores

        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def insert_sample_records(self):
        sample_scores = [{'player_name': 'paichiwo', 'score': i * 100} for i in range(1, 11)]
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        data['scores'].extend(sample_scores)
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
