import requests
import os
import db
import scrape
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv(verbose=True)
env_path = Path('.') / '.env'

class Bingo():

    def __init__(self):
        self.bingo_words = db.get_bingo_words()
        # self.score = score

    def score_list(self):
        response = []
        for word in self.bingo_words:
            if word[1]:
                response.append(f'- ~~{word[0]}~~')
            else:
                response.append(f'- {word[0]}')
        return response

    def scores(self):
        if self.bingo_words:
            response = ['!BINGO scores are in!']
            response.extend(self.score_list())
            response.append(f'{db.count_bingo_words(False)} left to go!')
            return "\n".join(response)
        return "Nothing yet. Add some words."

    def cross(self, word):
        if self.bingo_words:
            db.update_bingo_words(word, True)
            self.bingo_words = db.get_bingo_words()
            if db.count_bingo_words(True) == db.count_all_bingo_words():
                response = [f'We got {word} !BINGO']
                response.extend(self.score_list())
                response.append(f'Game over! Game has been reset')
                self.reset()
                return "\n".join(response)
            return f'We got {word} !BINGO'

    def info(self, word):
        time = db.get_bingo_result(word)
        time = datetime.today().date() - time[2]
        return f'Total of {time.days} days, since last mention of "{word}"'

    def reset(self):
        db.reset_bingo_words()
        return f'!BINGO is reset!'

    def add(self, word):
        if not db.get_bingo_result(word):
            db.insert_bingo_words(word)
            return f'{word} added! {len(self.bingo_words) + 1} words in the !BINGO'
        return 'Already in'

    def remove(self, word):
        if db.get_bingo_result(word):
            db.remove_bingo_words(word)
            if db.count_bingo_words(True) == db.count_all_bingo_words():
                self.bingo_words = db.get_bingo_words()
                response = [f'You cheating bastard!']
                response.extend(self.score_list())
                response.append(f'Game over! Game has been reset')
                self.reset()
                return "\n".join(response)
            return f'{word} removed! {len(self.bingo_words) - 1} words in the !BINGO'
        return 'No such word !Bingo'
        

class Finance():

    def __init__(self, symbol, symbol_two = 'USD'):
        self.symbol = symbol
        self.symbol_two = symbol_two
        self.api_key = os.getenv('API_KEY')

    def response(self, status):
        if status != 200:
            return False
        return True

    def multiply_price(self, price, multi):
        return str(float(price) * multi)

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
            response = response.split(".")
            response = f"{response[0]}.{response[1][:2]}"
            if self.symbol.lower() == "gme":
                response = self.multiply_price(response, 2)
            response = f'Price for {self.symbol.upper()} is {response} USD!'
            return response

    def quote_price(self):
        url = 'https://www.alphavantage.co/query?'
        response = requests.get(f'{url}function=CURRENCY_EXCHANGE_RATE&from_currency={self.symbol}&to_currency={self.symbol_two}&apikey={self.api_key}')
        if not self.response(response.status_code):
            return "Whoops, that didn't work!"
        response = response.json().get('Realtime Currency Exchange Rate')
        if not response:
            return "Try different abbrevation?"
        else:
            response = response['5. Exchange Rate']
            response = response.split(".")
            response = f"{response[0]}.{response[1][:2]}"
            response = f'Price for {self.symbol.upper()} is {response} {self.symbol_two}!'
            return response

def pixel_planet(planet=None):
    if planet:
        return scrape.scrape_pixel_planet(planet)
    else:
        return scrape.scrape_pixel_random()

def depicted(depict=None):
    if depict:
        return scrape.scrape_depicted(depict)
    else:       
        return scrape.scrape_depicted_random()