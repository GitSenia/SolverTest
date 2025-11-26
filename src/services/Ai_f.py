from groq import Groq
from dotenv import load_dotenv
import os
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
