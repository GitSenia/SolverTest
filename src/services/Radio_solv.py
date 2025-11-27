from bs4 import BeautifulSoup
from src.services.Ai_f import solve_question

def solv_radio(soup: BeautifulSoup):
    qtext_div = soup.find("div", class_="qtext")
    print(qtext_div)
    if not qtext_div or not qtext_div.text.strip():
        print("Вопрос содержит только изображение, пропускаем")
        return None  # или любое другое обозначение пропуска

    question = qtext_div.text.strip()
    answer = [a.text for a in soup.find_all("label", class_="ms-1")]
    print(question, answer)

    while True:
        ar_1 = solve_question(question, answer)
        if not ar_1:
            continue

        if ar_1[0].isdigit():
            num = int(ar_1.split(".")[0]) - 1
            print(num)
            return num


def solv_checkbox(soup: BeautifulSoup):
    qtext_div = soup.find("div", class_="qtext")
    if not qtext_div or not qtext_div.text.strip():
        print("Вопрос содержит только изображение, пропускаем")
        return None

    question = qtext_div.text.strip()
    answer = [a.text for a in soup.find_all("div", class_="flex-fill")]
    print(question, answer)

    while True:
        ar_1 = solve_question(question, answer)
        if not ar_1:
            continue

        numbers = []
        for x in ar_1.split(","):
            x = x.strip()
            if x and x[0].isdigit():
                num = int(x.split(".")[0]) - 1
                numbers.append(num)

        if numbers:
            print(numbers)
            return numbers



#
# q = "Какие из следующих алгоритмов относятся к методам обучения с учителем?"
#
# ans = ["Метод опорных векторов",
#        "Метод главных компонент",
#        "Случайный лес",
#        "Логистическая регрессия",
#         "K-средних"
#        ]
#
# result = solve_question(q, ans)
# print("Ответ нейросети:", result)
#
# #
# #
