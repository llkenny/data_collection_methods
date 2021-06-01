import pymongo
from pymongo import MongoClient
import pandas as pd
 
client = MongoClient('127.0.0.1:27018')
db = client.products_database

products = db.products

df = pd.read_csv('./2/result.csv')


def insert_one_product(product):
    """Добавление одного продукта"""
    db.collection.insert_one({
        'Наименование продукта': product['Наименование продукта'],
        'Качество': product['Качество'],
        'Категория продукта': product['Категория продукта'],
        'Подкатегория продукта': product['Подкатегория продукта'],
        'Безопасность': product['Безопасность'],
        'Общий балл': product['Общий балл'],
        'Сайт': product['Сайт']
    })


def import_products(df):
    """Обновление продуктов из DataFrame"""
    for index, row in df.iterrows():
        db.collection.update_one({'Наименование продукта': row['Наименование продукта']},
                                 {'$set':
                                  {'Качество': row['Качество'],
                                   'Категория продукта': row['Категория продукта'],
                                   'Подкатегория продукта': row['Подкатегория продукта'],
                                   'Безопасность': row['Безопасность'],
                                   'Общий балл': row['Общий балл'],
                                   'Сайт': row['Сайт']}},
                                 upsert=True)


def print_all_products():
    """Вывод всех продуктов"""
    for item in db.collection.find():
        print(item)


def print_products_more_than_rating(rating: int):
    """Вывод продуктов с рейтингом более rating по 100-бальной шкале"""
    five_scale = rating / 20  # По 5-и бальной шкале
    query_1 = {"Общий балл": {'$gt': str(rating)}}
    query_2 = {"Общий балл": {'$gt': str(five_scale), '$lte': '5'}}
    for item in db.collection.find({'$or': [query_1, query_2]}):
        print(item)


import_products(df)
print_all_products()

print_products_more_than_rating(75)
