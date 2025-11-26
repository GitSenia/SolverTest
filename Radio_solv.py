import requests
from bs4 import BeautifulSoup
from Ai_f import solve_question

def solv_radio(soup: BeautifulSoup):
    question = soup.find("div", class_="qtext").text.strip()
    answer = [a.text for a in soup.find_all("label", class_="ms-1")]
    print(question, answer)
    while True:
        ar_1 = solve_question(question, answer)
        if not ar_1:
            continue

        # извлекаем число из начала строки
        if ar_1[0].isdigit():
            num = int(ar_1.split(".")[0]) - 1
            print(num)
            return num
        # иначе повторяем запрос



def solv_checkbox(soup: BeautifulSoup):
    question = soup.find("div", class_="qtext").text.strip()
    answer = [a.text for a in soup.find_all("div", class_="flex-fill")]
    print(question, answer)
    while True:
        ar_1 = solve_question(question, answer)
        if not ar_1:
            continue  # если пусто — повторяем запрос

        # пытаемся извлечь числа из строки
        numbers = []
        for x in ar_1.split(","):
            x = x.strip()
            if x and x[0].isdigit():  # проверяем, что начинается с цифры
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
