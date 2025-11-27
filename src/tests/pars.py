from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import config.config as c
from dotenv import load_dotenv
import os
load_dotenv()


def fetch_preflight_form(session, cmid: int):
    quiz_view_url = f"https://lms.bsuir.by/mod/quiz/view.php?id={cmid}"

    # 1. GET страница теста
    resp = session.get(quiz_view_url)
    print("[1/2] GET страница теста, статус:", resp.status_code)

    soup = BeautifulSoup(resp.text, "lxml")

    # 2. Находим кнопку для начала попытки
    btn = soup.find("button", string=lambda x: x and ("тест" in x.lower() or "попыт" in x.lower()))
    if not btn:
        raise Exception("Не найдена кнопка 'Пройти тест' или 'Продолжить попытку'!")

    form = btn.find_parent("form")
    action = form["action"]
    payload = {inp.get("name"): inp.get("value") for inp in form.find_all("input") if inp.get("name")}

    # 3. POST первый шаг
    r = session.post(action, data=payload, allow_redirects=False)
    print("[2/2] POST первый шаг, статус:", r.status_code)

    # 4. Получаем HTML формы preflight
    soup2 = BeautifulSoup(r.text, "lxml")
    preflight_form = soup2.find("form", id="mod_quiz_preflight_form")
    if not preflight_form:
        raise Exception("Форма preflight не найдена после первого POST!")

    # 5. Вернем HTML формы и payload
    inputs = {inp.get("name"): inp.get("value") for inp in preflight_form.find_all("input") if inp.get("name")}
    form_html = str(preflight_form)

    return inputs, form_html


# Пример использования:
if __name__ == "__main__":
    session = requests.Session()
    session.post(c.url_login, data={'username': os.getenv("STUDENT_NUMBER"), 'password': os.getenv("PASSWORD")},allow_redirects=True)
    cmid = 305095  # замените на ваш cmid
    inputs, form_html = fetch_preflight_form(session, cmid)
    print("Inputs preflight:", inputs)
    print("HTML формы preflight (первые 1000 символов):\n", form_html[:1000])
