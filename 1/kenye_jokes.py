"""
Сделайте 100 get запрос к ссылке (endpoint) - https://api.kanye.rest/
Создайте словарь в питоне - пример: {'No':1, 'Joke': 'some kayne joke'}, не забиваем, что к каждой шутке прилагается номер!!)
И сохраните в json формате, который прикрепите к pull request (вместе с кодом).
"""

import requests
import json
from time import sleep

url = 'https://api.kanye.rest/'

jokes = []

for i in range(1, 101):
    data = requests.get(url).json()
    jokes.append({'No': i, 'Joke': data['quote']})
    sleep(1)

with open('kenye_jokes.json', 'w') as f:
    json.dump(jokes, f, indent=4)
