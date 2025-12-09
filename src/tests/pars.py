from requests import Session
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from src.bot_tg import config as c
from src.services.servises import type_of_batton
from src.services.url_create import get_attempt
from src.services.count_questions import count_questions


load_dotenv()

def submit_test(id:int, user_name:str, password:str):
    session = Session()
    session.post(c.url_login, data={'username': user_name, 'password': password}, allow_redirects=True)
    """
    Автоматическое прохождение теста.
    session: requests.Session с авторизацией
    url_test: URL страницы теста
    pages: количество страниц теста
    """
    url_d=get_attempt(session,id)
    pages = count_questions(url_d.get("attempt_url"),session)

    for i in range(pages):
        response = session.get(f"https://lms.bsuir.by/mod/quiz/attempt.php?attempt={url_d.get("attempt_id")}&cmid={id}&page={i}")
        soup = BeautifulSoup(response.text, "lxml")

        # Получаем правильные ответы (число или список чисел)
        correct_answers = type_of_batton(soup)
        if correct_answers is None:
            print(f"[Страница {i}] Вопрос с картинкой или пустой, пропускаем")
            continue



        post_data = {}

        for input_tag in soup.find_all("input"):
            name = input_tag.get("name")
            if not name:
                continue

            inp_type = input_tag.get("type")

            if inp_type == "radio" and name.endswith("_answer"):
                if isinstance(correct_answers, list):
                    post_data[name] = str(correct_answers[0])
                else:
                    post_data[name] = str(correct_answers)

            elif "_choice" in name:
                index = int(name.split("choice")[-1])
                post_data[name] = 1 if isinstance(correct_answers, list) and index in correct_answers else 0

            elif inp_type == "text":
                # вот здесь заполняем текстовые ответы
                post_data[name] = correct_answers


            elif name.endswith("_:sequencecheck"):
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



if __name__ == "__main__":
    submit_test(c.id_APEC,os.getenv("STUDENT_NUMBER"),os.getenv("PASSWORD"))
