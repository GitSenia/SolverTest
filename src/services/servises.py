import logging

from bs4 import BeautifulSoup
from src.services.Radio_solv import solv_radio
from src.services.Radio_solv import solv_checkbox
from src.services.Radio_solv import solv_text

def type_of_batton(soup:BeautifulSoup):


    if soup.find("input", {"type": "text"}):
        return solv_text(soup)

    a = soup.find("div", class_="r0")
    if a is None:
        logging.debug("данный тип вопросов не поддержтвается")
        return None

    a_2=a.find_all("input")
    a_type= []
    for b in a_2:
        a_type.append(b.get("type"))

    if 'radio' in a_type:
        return  solv_radio(soup)
    if 'checkbox' in a_type:
        return solv_checkbox(soup)
    else:
        logging.debug("пока не продуман такой тип заполнения вопросов")
        return None


