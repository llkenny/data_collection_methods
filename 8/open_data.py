import requests
import zipfile
import pandas as pd

class GosUslugi():

    def __init__(self):
        self.url = 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=1099123'
        self.path = '8/data.zip'
        self.file_name = 'data-6112-2021-05-25.xlsx'


    def fetch(self):
        r = requests.get(self.url, allow_redirects=True)
        open(self.path, 'wb').write(r.content)


    def unzip(self):
        with zipfile.ZipFile(self.path, 'r') as zip_ref:
            zip_ref.extractall('8/')


    def convert(self):
        data_xls = pd.read_excel(f'8/{self.file_name}', index_col=None)
        data_xls.to_csv('8/csvfile.csv', encoding='utf-8', index=False)


    def read(self):
        df = pd.read_csv('8/csvfile.csv')
        print(df.head())
