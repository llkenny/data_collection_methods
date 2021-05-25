"""
2. Изучить список открытых API.
    Найти среди них любое, требующее авторизацию (любого типа).
    Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import requests
import json
import time

apiKey = ''
privateKey = ''
ts = time.time()
_hash = f'{hash(ts)}{hash(privateKey)}{hash(apiKey)}'
url = f'https://gateway.marvel.com:443/v1/public/1011334/comics?apikey={apiKey}&ts={ts}&hash={_hash}'

req = requests.get(url)
data = json.loads(req.text)

with open('free_auth_api.json', 'w') as fp:
    json.dump(data, fp,  indent=4)
