from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs,urljoin

def get_attempt(session, cmid: int):


    quiz_view_url = f"https://lms.bsuir.by/mod/quiz/view.php?id={cmid}"

    print(f"[1/3] GET страница теста: {quiz_view_url}")
    resp = session.get(quiz_view_url)
    print(f"Статус ответа: {resp.status_code}")

    soup = BeautifulSoup(resp.text, "lxml")

    btn = soup.find("button", string=lambda x: x and ("тест" in x.lower() or "попыт" in x.lower()))
    if not btn:
        raise Exception("Не найдено кнопки 'Пройти тест' или 'Продолжить попытку'!")

    form = btn.find_parent("form")
    action = form["action"]
    payload = {inp.get("name"): inp.get("value") for inp in form.find_all("input") if inp.get("name")}

    print(f"[2/3] POST первый шаг на {action}")
    print(f"Данные формы: {payload}")
    r = session.post(action, data=payload, allow_redirects=False)
    print(f"Статус: {r.status_code}, заголовки: {r.headers}")

    # Проверяем, вернул ли Moodle редирект на attempt.php
    loc = r.headers.get("Location")
    if loc and "attempt.php" in loc:
        attempt_url = requests.compat.urljoin(action, loc)
        print(f"Редирект сразу на attempt.php: {attempt_url}")
    else:
        # Если редиректа нет — обрабатываем preflight
        soup = BeautifulSoup(r.text, "lxml")
        preflight_form = soup.find("form", id="mod_quiz_preflight_form")
        if not preflight_form:
            raise Exception("Не найден preflight, и нет редиректа на attempt.php")

        action = preflight_form["action"]
        payload = {inp.get("name"): inp.get("value") for inp in preflight_form.find_all("input") if inp.get("name")}
        payload["submitbutton"] = "Начать попытку"

        print(f"[3/3] POST preflight на {action}")
        print(f"Inputs preflight: {payload}")

        r2 = session.post(action, data=payload, allow_redirects=False)
        print(f"Статус: {r2.status_code}, заголовки: {r2.headers}")

        loc = r2.headers.get("Location")
        if not loc or "attempt.php" not in loc:
            raise Exception("Moodle снова не вернул редирект на attempt.php")
        attempt_url = requests.compat.urljoin(action, loc)

    qs = parse_qs(urlparse(attempt_url).query)
    attempt_id = int(qs["attempt"][0])
    page = int(qs.get("page", [0])[0])

    return {
        "attempt_url": attempt_url,
        "attempt_id": attempt_id,
        "page": page
    }


# session = Session()
# session.post(c.url_login, data={'username': os.getenv("STUDENT_NUMBER"), 'password': os.getenv("PASSWORD")}, allow_redirects=True)
# print(get_attempt(session,c.mid))
#
