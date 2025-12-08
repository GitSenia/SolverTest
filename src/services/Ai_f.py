from groq import Groq
from dotenv import load_dotenv
import os
import re
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
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,           # точный ответ
        max_completion_tokens=256,
        top_p=1,
        reasoning_effort="medium",
        stream=False,            # выключаем стрим — нам нужен результат сразу
    )

    return completion.choices[0].message.content.strip()

def solve_question_text(question: str) -> str:


    prompt = (

        f"Найди одно слово, которое подходит к вопросу. Выводи только это слово, без пояснений, пробелов и кавычек: {question}"
    )




    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,           # точный ответ
        max_completion_tokens=1000,
        top_p=1,
        # reasoning_effort="medium",
        stream=False,            # выключаем стрим — нам нужен результат сразу
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

