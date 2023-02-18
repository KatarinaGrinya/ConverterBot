import requests
import json
from configur import keys


class APIExeption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str,):
        if quote == base:
            raise APIExeption(f'Невозможно перевести одинаковые валюты {base}. ')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество валюты {amount}')

        if amount <= 0:
            raise APIExeption(f'Количество валюты не может быть меньше/равно 0')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        interm_base = json.loads(r.content)[keys[base]]
        total_base = interm_base * amount
        return round(total_base, 2)

class DeclinasionByCases:
    def __init__(self, word, num):
        self.word = word
        self.num = num

    def incline(self):
        if self.word != 'евро':
            if (2 <= self.num % 10 <= 4 and self.num % 100 not in [12, 13, 14]) or not self.num.is_integer():
                return 'рубля' if self.word == 'рубль' else self.word + 'a'
            if (self.num % 10 == 0 or 5 <= self.num % 10 <= 9 or 11 <= self.num % 100 <= 14) and self.num.is_integer():
                return 'рублей' if self.word == 'рубль' else self.word + 'ов'
        return self.word
