
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

class Finance():

    def __init__(self, symbol, symbol_two = 'USD'):
        self.symbol = symbol
        self.symbol_two = symbol_two
        self.api_key = os.getenv('API_KEY')

    def response(self, status):
        if status != 200:
            return False
        return True

    def quote_stock(self):
        url = 'https://www.alphavantage.co/query?'
        response = requests.get(f'{url}function=GLOBAL_QUOTE&symbol={self.symbol}&apikey={self.api_key}')

        if not self.response(response.status_code):
            return "Whoops, that didn't work!"

        response = response.json().get('Global Quote')

        if not response:
            return "Try different abbrevation?"
        else:
            response = response['05. price']
            response = f'Price for {self.symbol.upper()} is {response} USD!'
            return response

    def quote_crypto(self):
        url = 'https://www.alphavantage.co/query?'
        response = requests.get(f'{url}function=CURRENCY_EXCHANGE_RATE&from_currency={self.symbol}&to_currency={self.symbol_two}&apikey={self.api_key}')

        if not self.response(response.status_code):
            return "Whoops, that didn't work!"

        response = response.json().get('Realtime Currency Exchange Rate')

        if not response:
            return "Try different abbrevation?"
        else:
            response = response['5. Exchange Rate']
            response = f'Price for {self.symbol.upper()} is {response} {self.symbol_two}!'
            return response

