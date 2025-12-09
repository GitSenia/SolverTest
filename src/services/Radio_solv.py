
from bs4 import BeautifulSoup
from src.services.Ai_f import solve_question,solve_question_text

def solv_radio(soup: BeautifulSoup, max_attempts=10):

    qtext_div = soup.find("div", class_="qtext")
    if not qtext_div or not qtext_div.text.strip():
        print("Вопрос содержит только изображение или текст отсутствует, пропускаем")
        return None

    question = qtext_div.text.strip()

    # ИСПРАВЛЕНО: варианты картываем правильно
    answers = [
        div.text.strip()
        for div in soup.find_all("div", class_="flex-fill")
        if div.text.strip()
    ]
    if not answers:
        answers = [
            div.text.strip()
            for div in soup.find_all("label", class_="ms-1")
            if div.text.strip()
        ]


    print(question)
    print(answers)

    if not answers:
        print("Варианты ответа не найдены, пропускаем")
        return None

    for attempt in range(1, max_attempts + 1):
        print(f"Попытка {attempt}")
        result = solve_question(question, answers)
        print(result)
        if not result:
            continue

        if result[0].isdigit():
            num = int(result.split(".")[0]) - 1
            print(f"Выбран ответ: {num}")
            return num

    print("Не удалось определить правильный ответ")
    return None



def solv_checkbox(soup: BeautifulSoup, max_attempts=10):

    qtext_div = soup.find("div", class_="qtext")
    if not qtext_div or not qtext_div.text.strip():
        print("Вопрос содержит только изображение или текст отсутствует, пропускаем")
        return None

    question = qtext_div.text.strip()

    answers = [
        div.text.strip()
        for div in soup.find_all("div", class_="flex-fill")
        if div.text.strip()
    ]

    print(question)
    print(answers)

    if not answers:
        print("Варианты ответа не найдены, пропускаем")
        return None

    for attempt in range(1, max_attempts + 1):
        print(f"Попытка {attempt}")
        result = solve_question(question, answers)
        if not result:
            continue

        nums = []
        parts = result.replace(",", " ").split()

        for x in parts:
            if x.isdigit():
                nums.append(int(x) - 1)

        if nums:
            print(f"Выбраны ответы: {nums}")
            return nums

    print("Не удалось определить ответы")
    return None


def solv_text(soup: BeautifulSoup, max_attempts=5):
    qtext_div = soup.find("div", class_="qtext")
    if not qtext_div or not qtext_div.text.strip():
        print("Вопрос с текстовым ответом пустой, пропускаем")
        return None

    question = qtext_div.text.strip()
    print(question)


    answer = solve_question_text(question)
    print(question)
    print(answer)



    return answer





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
