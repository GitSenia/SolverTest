import requests
from bs4 import BeautifulSoup

import logging

from requests import Session
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from src.bot_tg import config as c
import re




load_dotenv()


session = Session()
str = session.post(c.url_login, data={'username': "32850203", 'password': "Shilov#Arseni5"}, allow_redirects=True)
soup = BeautifulSoup(str.text, 'lxml')
soup1=soup.find_all(class_=re.compile("coursebox"))






# Пример использования
def test_find(session: Session):
    tests_for_curs={}
    courseboxes = soup.find_all(class_=re.compile("coursebox"))
    for entry in courseboxes:

        link = entry.find(class_="info").find(class_="aalink").get("href")
        get_link = session.get(link)
        lxml_link = BeautifulSoup(get_link.text, 'lxml')
        name = lxml_link.find("div", class_="page-header-headings").text.strip("\n")
        link_quiz = lxml_link.find_all("li", class_="quiz")
        if not link_quiz:
            continue

        curs={}
        for l in link_quiz:
            name_test=l.find("span",class_="instancename")
            curs[name_test.text]=(l.get("data-id"))

        tests_for_curs[name] = curs


    print(tests_for_curs)




test_find(session)


