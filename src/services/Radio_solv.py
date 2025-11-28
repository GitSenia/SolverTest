from bs4 import BeautifulSoup
from src.services.Ai_f import solve_question

from bs4 import BeautifulSoup
from src.services.Ai_f import solve_question

def solv_radio(soup: BeautifulSoup, max_attempts=10):
    """
    Решает вопросы с одним выбором (radio).
    Если вопрос только с изображением или без текста — возвращает None.
    """
    qtext_div = soup.find("div", class_="qtext")
    if not qtext_div or not qtext_div.text.strip():
        print("Вопрос содержит только изображение или текст отсутствует, пропускаем")
        return None

    question = qtext_div.text.strip()
    answers = [a.text.strip() for a in soup.find_all("label", class_=" ms-1") if a.text.strip()]
    print(question)
    print(answers)


    if not answers:
        print("Варианты ответа не найдены, пропускаем")
        return None

    print(f"Вопрос (radio): {question}")
    print(f"Варианты ответа: {answers}")

    for attempt in range(1, max_attempts + 1):
        print(f"Попытка {attempt}")
        result = solve_question(question, answers)
        if not result or not result.strip():
            continue

        if result[0].isdigit():
            num = int(result.split(".")[0]) - 1
            print(f"Выбран ответ: {num}")
            return num

    print("Не удалось определить правильный ответ после нескольких попыток")
    return None


def solv_checkbox(soup: BeautifulSoup, max_attempts=10):
    """
    Решает вопросы с множественным выбором (checkbox).
    Если вопрос только с изображением или без текста — возвращает None.
    """
    qtext_div = soup.find("div", class_="qtext")
    if not qtext_div or not qtext_div.text.strip():
        print("Вопрос содержит только изображение или текст отсутствует, пропускаем")
        return None

    question = qtext_div.text.strip()
    answers = [a.text.strip() for a in soup.find_all("div", class_="flex-fill") if a.text.strip()]
    print(question)
    print(answers)
    if not answers:
        print("Варианты ответа не найдены, пропускаем")
        return None

    print(f"Вопрос (checkbox): {question}")
    print(f"Варианты ответа: {answers}")

    for attempt in range(1, max_attempts + 1):
        print(f"Попытка {attempt}")
        result = solve_question(question, answers)
        if not result or not result.strip():
            continue

        numbers = []
        # Разделяем ответ через запятую и пробел, безопасно обрабатываем
        parts = [p.strip() for p in result.replace(",", " ").split()]
        for x in parts:
            if x.isdigit():
                numbers.append(int(x) - 1)

        if numbers:
            print(f"Выбраны ответы: {numbers}")
            return numbers

    print("Не удалось определить правильные ответы после нескольких попыток")
    return None


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
