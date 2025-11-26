from bs4 import BeautifulSoup
import requests
from requests import Session
import config.config as c
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()

def get_attempt(session, cmid: int):
    """
    Принимает только cmid (ID курса/теста).
    Возвращает словарь:
    {
        "attempt_url": "...",
        "attempt_id": 589701,
        "page": 0
    }
    """

    quiz_view_url = f"https://lms.bsuir.by/mod/quiz/view.php?id={cmid}"

    # 1. Открываем страницу теста
    resp = session.get(quiz_view_url)
    soup = BeautifulSoup(resp.text, "lxml")

    # 2. Ищем любую "кнопку теста"
    btn = soup.find("button", string=lambda x: x and (
        "тест" in x.lower() or "попыт" in x.lower()
    ))

    if not btn:
        raise Exception("Не найдено кнопки 'Пройти тест' или 'Продолжить попытку'!")

    form = btn.find_parent("form")
    action = form["action"]

    # 3. Собираем поля формы
    payload = {
        inp.get("name"): inp.get("value")
        for inp in form.find_all("input") if inp.get("name")
    }

    # 4. Делаем POST на startattempt.php (редирект отключён)
    r = session.post(action, data=payload, allow_redirects=False)

    # 5. Moodle отдаёт redirect на attempt.php
    loc = r.headers.get("Location")
    if not loc:
        raise Exception("Moodle не вернул redirect на attempt.php")

    attempt_url = requests.compat.urljoin(quiz_view_url, loc)

    # Пример: attempt.php?attempt=589701&page=0


    qs = parse_qs(urlparse(attempt_url).query)
    attempt_id = int(qs["attempt"][0])
    page = int(qs["page"][0]) if "page" in qs else 0

    return {
        "attempt_url": attempt_url,
        "attempt_id": attempt_id,
        "page": page
    }




# session = Session()
# session.post(c.url_login, data={'username': os.getenv("STUDENT_NUMBER"), 'password': os.getenv("PASSWORD")}, allow_redirects=True)
# print(get_attempt(session,c.mid))
#
