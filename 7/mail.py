"""
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика,
и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма, текст письма)
"""

from selenium import webdriver
import time
import pandas as pd

mailId = ''
password = ''


driver = webdriver.Chrome('7/chromedriver')
driver.get("https://account.mail.ru/login?page=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox&allow_external=1")
time.sleep(5)

username_field = driver.find_element_by_name('username')
username_field.send_keys(mailId)
username_field.submit()

time.sleep(5)
password_field = driver.find_element_by_name('password')
password_field.send_keys(password)
password_field.submit()
time.sleep(20)

emails = driver.find_elements_by_css_selector('div.llc__container')
data = []
for i in emails:
    try:
        sender = i.find_element_by_xpath('div/div[1]/span').text
        title = i.find_element_by_xpath('//span[1]/span').text
        message = i.find_element_by_xpath('//span[2]/span').text
        date = i.find_element_by_xpath('div/div[6]').text

        data.append({
            'sender': sender,
            'title': title,
            'message': message,
            'date': date
        })
    except:
        pass

df = pd.DataFrame(data)
df.to_csv('7/mail.csv')
