"""
1. Посмотреть документацию к API GitHub,
    разобраться как вывести список репозиториев для конкретного пользователя,
    сохранить JSON-вывод в файле *.json.
"""
import requests
import json

url = 'https://api.github.com/users/llkenny/repos'
req = requests.get(url)
data = json.loads(req.text)
names = [item['name'] for item in data]
print(names)

with open('github_repos.json', 'w') as fp:
    json.dump(data, fp,  indent=4)
