from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urljoin

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from requests.compat import urljoin
import requests

def get_attempt(session, cmid: int):
    """
    Получение URL для попытки теста.
    Работает с Moodle, учитывает редирект сразу или форму preflight.
    Возвращает словарь:
    {
        "attempt_url": str,
        "attempt_id": int,
        "page": int
    }
    """
    quiz_view_url = f"https://lms.bsuir.by/mod/quiz/view.php?id={cmid}"
    print(f"[1/3] GET страница теста: {quiz_view_url}")
    resp = session.get(quiz_view_url)
    print(f"Статус ответа: {resp.status_code}")

    soup = BeautifulSoup(resp.text, "lxml")
    btn = soup.find("button", string=lambda x: x and ("тест" in x.lower() or "попыт" in x.lower()))
    if not btn:
        raise Exception("Не найдено кнопки 'Пройти тест' или 'Продолжить попытку'!")

    form = btn.find_parent("form")
    action_url = form["action"]
    payload = {inp.get("name"): inp.get("value") for inp in form.find_all("input") if inp.get("name")}

    print(f"[2/3] POST первый шаг на {action_url}")
    print("Данные формы:", payload)
    r1 = session.post(action_url, data=payload, allow_redirects=False)
    print(f"Статус: {r1.status_code}, заголовки: {r1.headers}")

    # Проверяем редирект сразу
    loc = r1.headers.get("Location")
    if loc and "attempt.php" in loc:
        attempt_url = urljoin(action_url, loc)
        print(f"Редирект сразу на attempt.php: {attempt_url}")
    else:
        # Обработка preflight
        soup = BeautifulSoup(r1.text, "lxml")
        preflight_form = soup.find("form", id="mod_quiz_preflight_form")
        if not preflight_form:
            raise Exception("Не найден preflight, и нет редиректа на attempt.php")

        action_url = preflight_form["action"]
        payload = {inp.get("name"): inp.get("value") for inp in preflight_form.find_all("input") if inp.get("name")}
        payload["submitbutton"] = "Начать попытку"
        if "cancel" in payload:
            del payload["cancel"]

        print(f"[3/3] POST preflight на {action_url}")
        print("Inputs preflight:", payload)
        r2 = session.post(action_url, data=payload, allow_redirects=False)
        print(f"Статус: {r2.status_code}, заголовки: {r2.headers}")

        loc = r2.headers.get("Location")
        if not loc or "attempt.php" not in loc:
            raise Exception("Moodle снова не вернул редирект на attempt.php")
        attempt_url = urljoin(action_url, loc)

    qs = parse_qs(urlparse(attempt_url).query)
    attempt_id = int(qs["attempt"][0])
    page = int(qs.get("page", [0])[0])

    print("Попытка начата! attempt_url:", attempt_url)
    return {
        "attempt_url": attempt_url,
        "attempt_id": attempt_id,
        "page": page
    }

# Пример использования
