from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import requests

def _parse_attempt_url(url: str):
    qs = parse_qs(urlparse(url).query)
    attempt_id = int(qs["attempt"][0])
    page = int(qs["page"][0]) if "page" in qs else 0
    return {"attempt_url": url, "attempt_id": attempt_id, "page": page}

def get_attempt(session, cmid: int):
    """
    Возвращает словарь с attempt_url, attempt_id, page.
    Работает с кнопкой старта попытки Moodle.
    """

    quiz_view_url = f"https://lms.bsuir.by/mod/quiz/view.php?id={cmid}"
    resp = session.get(quiz_view_url)
    soup = BeautifulSoup(resp.text, "lxml")

    # Находим форму с кнопкой старта
    start_form = soup.find("form", action=lambda x: x and "startattempt.php" in x)
    if not start_form:
        raise Exception("Не найдена форма для старта попытки")

    action = start_form.get("action")
    payload = {inp.get("name"): inp.get("value") for inp in start_form.find_all("input") if inp.get("name")}

    # Отправляем POST, allow_redirects=True, чтобы попасть на attempt.php
    r = session.post(action, data=payload, allow_redirects=True)
    attempt_url = r.url

    # Парсим attempt_id и page из URL
    qs = parse_qs(urlparse(attempt_url).query)
    if "attempt" not in qs:
        raise Exception("Не удалось определить attempt_url после старта попытки")

    attempt_id = int(qs["attempt"][0])
    page = int(qs.get("page", [0])[0])
    return {"attempt_url": attempt_url, "attempt_id": attempt_id, "page": page}



# session = Session()
# session.post(c.url_login, data={'username': os.getenv("STUDENT_NUMBER"), 'password': os.getenv("PASSWORD")}, allow_redirects=True)
# print(get_attempt(session,c.mid))
#
