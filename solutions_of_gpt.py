from requests import Session
from bs4 import BeautifulSoup
import config as c
from servises import type_of_batton
from dotenv import load_dotenv
import os

load_dotenv()

def submit_test(session: Session, url_test: str, pages: int):
    """
    Автоматическое прохождение теста.
    session: requests.Session с авторизацией
    url_test: URL страницы теста
    pages: количество страниц теста
    """
    for i in range(pages):
        response = session.get(f"{url_test}&page={i}")
        soup = BeautifulSoup(response.text, "lxml")

        # Получаем правильные ответы (число или список чисел)
        correct_answers = type_of_batton(soup)


        post_data = {}

        # Берём все input'ы на странице
        for input_tag in soup.find_all("input"):
            name = input_tag.get("name")
            if not name:
                continue

            # Радио — одно число
            if name.endswith("_answer") and input_tag.get("type") == "radio":
                if isinstance(correct_answers, list):
                    post_data[name] = str(correct_answers[0])
                else:
                    post_data[name] = str(correct_answers)

            # Чекбоксы — несколько вариантов
            elif "_choice" in name:
                index = int(name.split("choice")[-1])
                post_data[name] = 1 if isinstance(correct_answers, list) and index in correct_answers else 0

            # Флажки и sequencecheck
            elif name.endswith("_:flagged") or name.endswith("_:sequencecheck"):
                post_data[name] = input_tag.get("value", "")

        # Обязательные поля Moodle
        for field in ["attempt", "sesskey", "thispage", "nextpage", "slots"]:
            tag = soup.find("input", {"name": field})
            if tag:
                post_data[field] = tag.get("value", "")

        post_data["timeup"] = 0
        post_data["mdlscrollto"] = ""

        # === Исправленный блок для кнопки "next" ===
        next_btn = soup.find("button", {"type": "submit"})
        if next_btn:
            post_data["next"] = next_btn.get_text(strip=True)
        else:
            next_input = soup.find("input", {"type": "submit"})
            if next_input:
                post_data["next"] = next_input.get("value", "Следующая страница")
            else:
                post_data["next"] = "Следующая страница"

        # URL для отправки
        url_post = soup.find("form").get("action")

        # Отправка POST
        response_post = session.post(url_post, data=post_data)
        print(f"Страница {i} отправлена, статус: {response_post.status_code}")


# === Использование ===
if __name__ == "__main__":
    session = Session()
    session.post(c.url_login, data={'username': os.getenv("STUDENT_NUMBER"), 'password': os.getenv("PASSWORD")}, allow_redirects=True)
    submit_test(session, c.url_test, pages=2)
