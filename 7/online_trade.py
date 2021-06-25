"""
Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, ОНЛАЙН ТРЕЙД и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome('7/chromedriver')
driver.get("https://www.onlinetrade.ru/")
time.sleep(5)

hits = driver.find_element_by_xpath('//*[@id="main_area"]/div[4]/div/div[4]')
hits.location_once_scrolled_into_view

items = hits.find_elements_by_css_selector('div.indexGoods__item')
data = []

def store_items():
    for i in items:
        title = i.find_element_by_css_selector('a.indexGoods__item__name').text.strip()
        price = i.find_element_by_css_selector('div.indexGoods__item__price span').text

        if title not in [t['title'] for t in data]:
            data.append({
                'title': title,
                'price': price
            })
    
    next = hits.find_element_by_css_selector('span.swiper-button-next.ic__hasSet.ic__hasSet__arrowNextBlue')
    if next is not None:
        next.click()

store_items()

df = pd.DataFrame(data)
df.to_csv('7/online-trade.csv')
