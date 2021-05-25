from bs4 import BeautifulSoup
import requests
import lxml
import json
from fake_headers import Headers
import pandas as pd

headers = Headers(headers=True).generate()

url_rskrf= 'https://rskrf.ru/ratings/produkty-pitaniya/'
url_rskrf_head = 'https://rskrf.ru'

def prepare_dataframe():
    """Подготовка пустого DataFrame"""
    return pd.DataFrame(columns=['Наименование продукта',
                                 'Категория продукта',
                                 'Подкатегория продукта',
                                 'Безопасность',
                                 'Качество',
                                 'Общий балл',
                                 'Сайт'])


def load_rskrf_item(url):
    """Загрузка элемента с сайта 'Роскачество'"""
    req = requests.get(url_rskrf_head + url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    df = prepare_dataframe()
    ds = pd.Series()
    if len(soup.select('p.product-subtitle')) > 0:
        ds['Наименование продукта'] = soup.select('p.product-subtitle')[0].string
    elif len(soup.select('h1.h1.product-title')) > 0:
        ds['Наименование продукта'] = soup.select('h1.h1.product-title')[0].string

    rating_items = soup.select('div.rating-item')
    ratings = {i.select('span')[0].string: i.select('span')[1].string for i in rating_items}

    param_1 = [value for key, value in ratings.items() if 'Общий рейтинг' in key]
    if len(param_1) > 0:
        ds['Общий балл'] = param_1[0]

    param_2 = [value for key, value in ratings.items() if 'безопасн' in key.lower()]
    if len(param_2) > 0:
        ds['Безопасность'] = param_2[0]

    param_3 = [value for key, value in ratings.items() if 'качество' in key.lower()]
    if len(param_3) > 0:
        ds['Качество'] = param_3[0]

    df = df.append(pd.Series(ds), ignore_index=True)
    return df


def load_rskrf_items(child_subcategory):
    url = child_subcategory['href']
    req = requests.get(url_rskrf_head + url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')
    urls = [i for i in soup.select('a') if i.has_attr('href')]
    urls = [i['href'] for i in urls if 'goods' in i['href']]

    return pd.concat([load_rskrf_item(i) for i in urls])


def load_rskrf_subcategory(subcategory, subcategory_title):
    """Загрузка подкатегории с сайта 'Роскачество'"""
    subcategory_url = subcategory['href']

    req = requests.get(url_rskrf_head + subcategory_url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    result = prepare_dataframe()

    for child in soup.select('div.category-item'):
        child_subcategory = child.select('a')[0]
        child_subcategory_title = child_subcategory.select('span.d-xl-none.d-block')[0].string
        child_df = load_rskrf_items(child_subcategory)
        child_df['Подкатегория продукта'] = child_subcategory_title
        result = pd.concat([result, child_df])

    return result


def load_rskrf():
    """Загрузка данных с сайта 'Роскачество'"""
    req = requests.get(url_rskrf, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    categories = soup.select('div.category-item')

    result = prepare_dataframe()

    for category in categories:
        subcategory = category.select('a')[0]
        df = load_rskrf_subcategory(subcategory, "")
        df['Категория продукта'] = subcategory.select('span')[1].string
        df['Сайт'] = url_rskrf_head
        result = pd.concat([result, df])
        # Сохранение частичных данных для защиты от потери соединения или блокировки
        result.to_csv('output_rskrf.csv')

    return result


url_roscontrol= 'https://roscontrol.com/category/produkti/#'
url_roscontrol_head = 'https://roscontrol.com/'


def load_roscontrol_item(url):
    """Загрузка элемента с сайта 'Росконтроль'"""
    req = requests.get(url_roscontrol_head + url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    df = prepare_dataframe()
    ds = pd.Series()
    if len(soup.select('h1.main-title.testlab-caption-products.util-inline-block')) > 0:
        ds['Наименование продукта'] = soup.select('h1.main-title.testlab-caption-products.util-inline-block')[0].string

    # Иногда выскакивает popup
    if len(soup.select('div.product__single-rev-total')) < 1:
        return df
    
    rating_items = soup.select('div.product__single-rev-total')[0]
    ds['Общий балл'] = rating_items.select('div.total')[0].string
    
    ratings = {i.select('div.rate-item__title')[0].string: i.select('span')[0].string for i in soup.select('div.rate-item.group')}

    param_2 = [value for key, value in ratings.items() if 'безопасн' in key.lower()]
    if len(param_2) > 0:
        ds['Безопасность'] = param_2[0]

    param_3 = [value for key, value in ratings.items() if 'качество' in key.lower()]
    if len(param_3) > 0:
        ds['Качество'] = param_3[0]

    df = df.append(pd.Series(ds), ignore_index=True)
    return df


def load_roscontrol_items(url):
    req = requests.get(url_roscontrol_head + url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')
    
    urls = [i for i in soup.select('a.block-product-catalog__item.js-activate-rate.util-hover-shadow.clear') if i.has_attr('href')]

    return pd.concat([load_roscontrol_item(i['href']) for i in urls])


def load_roscontrol_category(url):
    """Загрузка категории с сайта 'Росконтроль'"""
    
    req = requests.get(url_roscontrol_head + url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    result = prepare_dataframe()

    for child in soup.select('div.testlab-category')[0].select('a.catalog__category-item.util-hover-shadow'):
        child_url = child['href']
        child_title = child.select('div.catalog__category-name')[0].string
        child_df = load_roscontrol_items(child_url)
        child_df['Подкатегория продукта'] = child_title
        result = pd.concat([result, child_df])

    return result


def load_roscontrol():
    """Загрузка данных с сайта 'Роскачество'"""
    req = requests.get(url_roscontrol, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    categories = soup.select('div.main-container__cont.group')[0].select('a.catalog__category-item.util-hover-shadow')

    result = prepare_dataframe()

    for category in categories:
        category_url = category['href']
        category_title = category.select('div.catalog__category-name')[0].string
        df = load_roscontrol_category(category_url)
        df['Категория продукта'] = category_title
        df['Сайт'] = url_roscontrol_head
        result = pd.concat([result, df])
        # Сохранение частичных данных для защиты от потери соединения или блокировки
        result.to_csv('output_roscontrol.csv')

    return result


df = load_rskrf()
df_roscontrol = load_roscontrol()

result = pd.concat([df, df_roscontrol])
result.to_csv('result.csv')
