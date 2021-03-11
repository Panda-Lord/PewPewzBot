
import requests
import os
# import json
from dotenv import load_dotenv
load_dotenv(verbose=True)
from pathlib import Path
env_path = Path('.') / '.env'

class Bingo():

    def __init__(self, bingo_words, scored_words, score):
        self.bingo_words = bingo_words
        self.scored_words = scored_words
        self.score = score

    def score_list(self):
        response = []
        left_count = 0
        for word in self.bingo_words:
            if word in self.scored_words:
                response.append(f'- ~~{word}~~')
            else:
                left_count += 1
                response.append(f'- {word}')
        response.append(f'{left_count} left to go!')
        return response

    def scores(self):
        response = ['Bingo scores are in!']
        response.extend(self.score_list())
        return "\n".join(response)

    def cross(self, word):
        return "BINGO!"

class Stock():

    def __init__(self, stock):
        self.stock = stock
        self.api_key = os.getenv('API_KEY')

    def quote(self):
        url = 'https://www.alphavantage.co/query?'

        response = requests.get(f'{url}function=GLOBAL_QUOTE&symbol={self.stock}&apikey={self.api_key}')

        return response.json()['Global Quote']

        
