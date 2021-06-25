
from pprint import pprint
from lxml import html
import requests
import time
from fake_headers import Headers
import pandas as pd

headers = Headers(headers=True).generate()

k_source = 'название источника'
k_title = 'наименование новости'
k_link = 'ссылка на новость'
k_date = 'дата публикации'

def prepare_dataframe():
    """Подготовка пустого DataFrame"""
    return pd.DataFrame(columns=[k_source,
                                 k_title,
                                 k_link,
                                 k_date])

def get_yandex():
    req = requests.get('https://yandex.ru', headers=headers)
    root = html.fromstring(req.text)
    news = root.xpath('//*[@id="news_panel_news"]')
    news_list = news[0].xpath('.//li')

    df = prepare_dataframe()
    for i in news_list:
        url = i.xpath('.//@href')[0]
        text = i.xpath('.//text()')[0]
        df = df.append({k_link: url, k_title: text}, ignore_index=True)
    df[k_source] = 'yandex'
    return df


def get_lenta():
    req = requests.get('https://lenta.ru/', headers=headers)
    root = html.fromstring(req.text)
    news = root.xpath('//*[@id="root"]/section[2]/div/div/div[1]')
    news_list = news[0].xpath(".//div[@class='item']")

    df = prepare_dataframe()
    for i in news_list:
        url = 'https://lenta.ru/' + i.xpath('.//@href')[0]
        text = i.xpath('.//text()')[1]
        date = i.xpath('.//time')[0].xpath('attribute::datetime')[0]
        df = df.append({k_link: url, k_title: text, k_date: date}, ignore_index=True)
    df[k_source] = 'lenta'
    return df


def get_mail():
    req = requests.get('https://mail.ru/', headers=headers)
    root = html.fromstring(req.text)
    news = root.xpath('//*[@id="grid:middle"]/div[2]/div[4]/div[1]/ul')
    news_list = news[0].xpath(".//li")

    df = prepare_dataframe()
    for i in news_list:
        url = i.xpath('.//@href')[0]
        # В списке попадается реклама
        if 'news.mail.ru' in url:
            text = i.xpath('.//text()')[1].rstrip() # Встречается перенос строки
            df = df.append({k_link: url, k_title: text}, ignore_index=True)
    df[k_source] = 'mail'
    return df

df_yandex = get_yandex()
df_lenta = get_lenta()
df_mail = get_mail()
result = pd.concat([df_yandex, df_lenta, df_mail])

result.to_csv('result.csv')
