import re

s = {('АПЭЦ', 'Шилин'): {'test2  Тест': '305095'}, ('ОМО', 'Голда'): {'Тест ': '324848'}, ('ПАС', 'Ломако'): {'Тест 1 ': '231421', 'Тест 2 ': '231436', 'Тест 3 ': '231451', 'Тест 4 ': '231466', 'Тест 5 ': '231481'}}

for sabject_teacher,values in s.items():
    print(sabject_teacher,values)




import requests
from bs4 import BeautifulSoup

import logging

from requests import Session
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import Dict,Tuple
import os

from src.bot_tg import config as c
import re





load_dotenv()










# Пример использования
def test_find(user_name:str, password:str) ->Dict[Tuple[str, str], Dict[str, str]]:
    tests_for_curs={}
    session = Session()
    str = session.post(c.url_login, data={'username':user_name, 'password': password}, allow_redirects=True)

    soup = BeautifulSoup(str.text, 'lxml')
    courseboxes = soup.find_all(class_=re.compile("coursebox"))
    all_quiz=[]
    for entry in courseboxes:

        link = entry.find(class_="info").find(class_="aalink").get("href")
        get_link = session.get(link)
        lxml_link = BeautifulSoup(get_link.text, 'lxml')
        name = lxml_link.find("div", class_="page-header-headings").text.strip("\n")

        logging.info(name)
        quiz_links = lxml_link.find_all("a", href=re.compile(r"/mod/quiz/view\.php\?id=\d+"))
        all_quiz.append(quiz_links)
        for a in quiz_links:
            href = a.get("href")
            match = re.search(r"id=(\d+)", href)
            quiz_id = match.group(1) if match else None
            title = a.text.strip()
            logging.info(f"Название: {title}, Ссылка: {href}, ID: {quiz_id}")

    return all_quiz


def test_find_2(user_name:str, password:str) ->Dict[Tuple[str, str], Dict[str, str]]:
    tests_for_curs={}
    session = Session()
    str = session.post(c.url_login, data={'username':user_name, 'password': password}, allow_redirects=True)

    soup = BeautifulSoup(str.text, 'lxml')
    courseboxes = soup.find_all(class_=re.compile("coursebox"))
    all_quiz=[]
    for entry in courseboxes:

        link = entry.find(class_="info").find(class_="aalink").get("href")
        get_link = session.get(link)
        lxml_link = BeautifulSoup(get_link.text, 'lxml')
        name = lxml_link.find("div", class_="page-header-headings").text.strip("\n")
        quiz_links = lxml_link.find_all("a", href=re.compile(r"/mod/quiz/view\.php\?id=\d+"))

        for a in quiz_links:
            href = a.get("href")
            all_quiz.append(href)


    return all_quiz

def test_find_3(user_name:str, password:str) ->Dict[Tuple[str, str], Dict[str, str]]:
    tests_for_curs={}
    session = Session()
    str = session.post(c.url_login, data={'username':user_name, 'password': password}, allow_redirects=True)

    get_link = session.get("https://lms.bsuir.by/course/view.php?id=8736")
    soup_pars = BeautifulSoup(get_link.text, 'lxml')

    return soup_pars

with open("file.txt", "w", encoding="utf-8") as f:
    f.write(test_find_3("32850203","Shilov#Arseni5").prettify())

# print(test_find_3("32850203","Shilov#Arseni5"))
# print(test_find("32850203","Shilov#Arseni5"))





# for key,values in test_find("32850203","Shilov#Arseni5").items():
#     name_for_subject = ""
#     name_of_teacher=key.split()[-1]
#     key=key.replace("(ДН)","").replace(name_of_teacher,"")
#     if key.find("."):
#         for i in key.split('.', 1)[0].split():
#             name_for_subject += i[0].upper()
#     print(name_of_teacher,name_for_subject,values)
#
#







