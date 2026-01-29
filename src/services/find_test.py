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










# Пример использования
def test_find(user_name:str, password:str):
    tests_for_curs={}
    session = Session()
    str = session.post(c.url_login, data={'username':user_name, 'password': password}, allow_redirects=True)

    soup = BeautifulSoup(str.text, 'lxml')
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

    tests_for_curs_pars={}
    for key, values in tests_for_curs.items():

        name_for_subject = ""
        name_of_teacher = key.split()[-1]
        key = key.replace("(ДН)", "").replace(name_of_teacher, "")

        for i in key.split('.', 1)[0].split():
            name_for_subject += i[0].upper()

        tests_for_curs_pars[(name_for_subject,name_of_teacher)] = values


    return tests_for_curs_pars





print(test_find("32850203","Shilov#Arseni5"))





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






