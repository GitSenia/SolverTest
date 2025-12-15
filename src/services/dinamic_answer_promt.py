import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os



def load_questions(json_file: str):
    # путь к папке, где лежит этот скрипт
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, json_file)

    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("questions", [])


questions_db = load_questions("ansver.json")


def find_similar_questions(question_text: str, questions_db: list, threshold=0.35, top_k=3):
    """
    Ищет похожие вопросы по косинусной схожести TF-IDF.
    """
    corpus = [q["questionText"] for q in questions_db]
    corpus.append(question_text)  # добавляем новый вопрос для сравнения

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(tfidf[-1], tfidf[:-1])[0]

    results = []
    for sim, q in zip(similarities, questions_db):
        if sim >= threshold:
            results.append((sim, q))

    results.sort(reverse=True, key=lambda x: x[0])
    return [q for _, q in results[:top_k]]

def f_prompt(question: str, answers: list[str], questions_db: list) -> str:
    """
    Формирует промпт для модели с few-shot.
    """
    similar = find_similar_questions(question, questions_db)

    prompt = (
        "Ты — эксперт по базам данных и SQL.\n"
        "Ты решаешь тестовое задание.\n"
        "Дай ТОЛЬКО номер правильного ответа без объяснений.\n\n"
    )

    # few-shot примеры
    if similar:
        prompt += "Примеры похожих вопросов с правильными ответами:\n\n"
        for q in similar:
            prompt += f"Вопрос: {q['questionText']}\n"
            for i, a in enumerate(q["answers"], 1):
                prompt += f"{i}. {a['answerText']}\n"
            correct_index = next((i + 1 for i, a in enumerate(q["answers"]) if a["isCorrect"]), None)
            if correct_index is None:
                continue  # пропускаем, если нет правильного ответа
            prompt += f"Правильный ответ: {correct_index}\n\n"

    # текущий вопрос
    prompt += f"Вопрос: {question}\n"
    prompt += "Варианты ответа:\n"
    for i, ans in enumerate(answers, 1):
        prompt += f"{i}. {ans}\n"

    return prompt




# print(f"Всего вопросов: {len(questions_db)}")
# print(f"Первый вопрос: {questions_db[0]['questionText']}")
# print("Ответы первого вопроса:")
# for i, a in enumerate(questions_db[0]['answers'], 1):
#     print(f"{i}. {a['answerText']} {'(правильный)' if a['isCorrect'] else ''}")
#
# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#
#
# test_question = "Какая логическая операция имеет обозначение A[XΘY]B?"
#
# similar = find_similar_questions(test_question, questions_db)
# print(f"Найдено похожих вопросов: {len(similar)}")
# for q in similar:
#     print("-", q['questionText'])
#
# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#
# answers_list = [
#     "тетта-соединение",
#     "декартово произведение",
#     "сравнение",
#     "пересечение",
#     "удаление"
# ]
#
# prompt = f_prompt(test_question, answers_list, questions_db)
# print(prompt)
#
# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
