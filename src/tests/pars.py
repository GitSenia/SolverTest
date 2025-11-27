from requests import Session
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

import config.config as c
from src.services.servises import type_of_batton
from src.services.url_create import get_attempt
from src.services.count_questions import count_questions

load_dotenv()

def submit_test(session: Session, cmid: int):
    """
    Автоматическое прохождение теста.
    session: requests.Session с авторизацией
    cmid: ID курса/теста
    """
    url_d = get_attempt(session, cmid)
    pages = count_questions(url_d["attempt_url"], session)

    for i in range(pages):
        attempt_id = url_d["attempt_id"]
        page_url = f"https://lms.bsuir.by/mod/quiz/attempt.php?attempt={attempt_id}&cmid={cmid}&page={i}"

        response = session.get(page_url)
        soup = BeautifulSoup(response.text, "lxml")

        # Получаем правильные ответы
        correct_answers = type_of_batton(soup)

        post_data = {}

        # Заполняем ответы
        for input_tag in soup.find_all("input"):
            name = input_tag.get("name")
            if not name:
                continue

            if name.endswith("_answer") and input_tag.get("type") == "radio":
                post_data[name] = str(correct_answers if isinstance(correct_answers, int) else correct_answers[0])

            elif "_choice" in name:
                index = int(name.split("choice")[-1])
                post_data[name] = 1 if isinstance(correct_answers, list) and index in correct_answers else 0

            elif name.endswith("_:flagged") or name.endswith("_:sequencecheck"):
                post_data[name] = input_tag.get("value", "")

        # Обязательные поля Moodle
        for field in ["attempt", "sesskey", "thispage", "nextpage", "slots"]:
            tag = soup.find("input", {"name": field})
            if tag:
                post_data[field] = tag.get("value", "")

        post_data["timeup"] = 0
        post_data["mdlscrollto"] = ""

        # Кнопка "Next"
        next_btn = soup.find("button", {"type": "submit"})
        if next_btn:
            post_data["next"] = next_btn.get_text(strip=True)
        else:
            next_input = soup.find("input", {"type": "submit"})
            post_data["next"] = next_input.get("value", "Следующая страница") if next_input else "Следующая страница"

        # URL формы для POST
        form = soup.find("form")
        if not form:
            raise Exception(f"Не найдена форма на странице {i}")
        url_post = form.get("action")

        # Отправка POST
        response_post = session.post(url_post, data=post_data)
        print(f"Страница {i} отправлена, статус: {response_post.status_code}")


if __name__ == "__main__":
    session = Session()
    login_data = {'username': os.getenv("STUDENT_NUMBER"), 'password': os.getenv("PASSWORD")}
    session.post(c.url_login, data=login_data, allow_redirects=True)
    submit_test(session, c.id_APEC)
