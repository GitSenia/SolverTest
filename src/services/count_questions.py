from bs4 import BeautifulSoup
from requests import Session
from dotenv import load_dotenv

load_dotenv()

def count_questions(attempt_url, session:Session):



    r = session.get(attempt_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Находим все элементы навигации вопросов
    qn_buttons = soup.find_all("a", class_="qnbutton")

    return len(qn_buttons)


# session = Session()
# session.post(c.url_login, data={'username': os.getenv("STUDENT_NUMBER"), 'password': os.getenv("PASSWORD")}, allow_redirects=True)
# t=get_attempt(session,c.mid)
# print(t)
# print(session.cookies)
# print(count_questions(t.get("attempt_url"),session))
