from requests import Session
from bs4 import BeautifulSoup
from Radio_solv import solv_radio
from Radio_solv import solv_checkbox

def type_of_batton(soup:BeautifulSoup):
    a = soup.find("div", class_="r0").find_all("input")
    a_type= []
    for b in a:
        a_type.append(b.get("type"))

    if 'radio' in a_type:
        return  solv_radio(soup)
    if 'checkbox' in a_type:
        return solv_checkbox(soup)


