import telebot
from telebot import types
import os
from dotenv import load_dotenv
load_dotenv()

from src.bot_tg.bot_f import start_test

# Твой токен
TOKEN = os.getenv("TOKEN_BOT")




bot = telebot.TeleBot(TOKEN)



users = {}



STATE_WAITING_NAME = "waiting_name"
STATE_WAITING_PASSWORD = "waiting_password"



@bot.message_handler(commands=['registration'])
def registration(message):
    chat_id = message.chat.id
    users[chat_id] = {"state": STATE_WAITING_NAME} # Устанавливаем состояние ожидания имени
    bot.send_message(chat_id, "Введите ваше имя:")

@bot.message_handler(func=lambda message: message.chat.id in users)
def handle_registration(message):
    chat_id = message.chat.id
    user_data = users[chat_id]

    if user_data["state"] == STATE_WAITING_NAME:
        user_data["name"] = message.text
        user_data["state"] = STATE_WAITING_PASSWORD
        bot.send_message(chat_id, "Введите ваш пароль:")

    elif user_data["state"] == STATE_WAITING_PASSWORD:
        user_data["password"] = message.text
        user_data["state"] = None  # Сбрасываем состояние
        bot.send_message(chat_id, f"Регистрация завершена успешно!\nИмя: {user_data['name']}\nПароль: {user_data['password']}")

        # Здесь можно сохранить данные в базу или файл
        print(f"Новый пользователь: {user_data['name']}, Пароль: {user_data['password']}")
        users.pop(chat_id)  # Убираем пользователя из словаря состояния, если не нужно хранить

@bot.message_handler(commands=['test'])
def test_solv(message):


    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("СУБД", callback_data="option1")
    btn2 = types.InlineKeyboardButton("САИО", callback_data="option2")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)

def callback(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("начать решать", callback_data="start_db")
    markup.add(btn1)
    markup2 = types.InlineKeyboardMarkup(row_width=2)
    btn2 = types.InlineKeyboardButton("начать решать", callback_data="start_db")
    markup2.add(btn2)
    if call.data=="option1":
        bot.send_message(call.message.chat.id, "СУБД:", reply_markup=markup)

    if call.data=="start_db":
        start_test()
        bot.send_message(call.message.chat.id, "решаю тест")





bot.infinity_polling()
