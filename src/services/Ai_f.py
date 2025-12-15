from groq import Groq
from dotenv import load_dotenv
import os
import re

from src.services.dinamic_answer_promt import f_prompt, questions_db,find_similar_questions

load_dotenv()


client = Groq(api_key=os.getenv("API_KEY"))


def solve_question(question: str, answers: list[str]) -> str:


    prompt = (
        "Ты решаешь тест. Дай только правильный номер ответа без объяснений.\n\n"
        f"Вопрос: {question}\n\n"
        "Варианты ответа:\n"
    )

    # нумерация вариантов
    for i, ans in enumerate(answers, start=1):
        prompt += f"{i}. {ans}\n"

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,           # точный ответ
        max_completion_tokens=3000,
        top_p=0.7,
        reasoning_effort="medium",
        stream=False,            # выключаем стрим — нам нужен результат сразу
    )

    return completion.choices[0].message.content.strip()

def solve_question_text(question: str) -> str:


    prompt = (

        f"Найди одно слово, которое подходит к вопросу. Выводи только это слово, без пояснений, пробелов и кавычек: {question}"
    )




    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,           # точный ответ
        max_completion_tokens=1500,
        top_p=0.7,
        # reasoning_effort="medium",
        stream=False,            # выключаем стрим — нам нужен результат сразу
    )


    return completion.choices[0].message.content.strip()

def solve_question_2(question: str, answers: list[str]) -> str:
    """
    Возвращает номер правильного ответа через GPT-OSS с few-shot.
    Если похожие вопросы не найдены — вызывает базовую функцию solve_question.
    Принимает только вопрос и список ответов.
    """
    # ищем похожие вопросы в глобальной базе
    similar = find_similar_questions(question, questions_db)

    # если похожих вопросов нет, вызываем базовую функцию
    if not similar:
        return solve_question(question, answers)

    # формируем промпт с few-shot
    prompt = f_prompt(question, answers, questions_db)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        top_p=0.6,
        max_completion_tokens=2024,
        reasoning_effort="medium",
        stream=False
    )

    return completion.choices[0].message.content.strip()





# def ars(c:str):
#     completion = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"Найди одно слово, которое подходит к вопросу. Выводи только это слово, без пояснений, пробелов и кавычек:{c}"
#             }
#         ],
#         temperature=0,
#         max_completion_tokens=400,
#         top_p=1,
#         reasoning_effort="medium",
#         stream=True,
#         stop=None
#     )
#
#     # for chunk in completion:
#     #     print(chunk.choices[0].delta.content or "", end="")
#     return completion.choices[0].delta.content

# q="Cлучайный процесс, в котором при фиксированном настоящем будущее состояние СМО не зависит от прошлого, называется Ответ Вопрос 7 процессом"
#
# sol = solve_question_text(q)
# print(sol)
#

