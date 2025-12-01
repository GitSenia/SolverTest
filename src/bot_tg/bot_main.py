import telebot
from telebot import types
import os
from dotenv import load_dotenv
import re

from src.db.DB_f import insert_user
from src.bot_tg.bot_f import start_test
from src.tests.pars import submit_test
from src.db.DB_f import user_info


load_dotenv()
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
        user_data["tg_id"] = message.from_user.id
        user_data["state"] = None  # Сбрасываем состояние

        insert_user(user_data['name'], user_data['password'],user_data["tg_id"])# обработчик ошибок нужно повесить
        bot.send_message(chat_id, f"Регистрация завершена успешно!\nИмя: {user_data['name']}\nПароль: {user_data['password']}")

        # Здесь можно сохранить данные в базу или файл
        print(f"Новый пользователь: {user_data['name']}, Пароль: {user_data['password']}")
        users.pop(chat_id)  # Убираем пользователя из словаря состояния, если не нужно хранить

@bot.message_handler(commands=['test'])
def test_solv(message: telebot.types.Message):



    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("СУБД", callback_data="option1")
    btn2 = types.InlineKeyboardButton("САИО", callback_data="option2")
    btn3 = types.InlineKeyboardButton("ОМО", callback_data="option3")
    btn4 = types.InlineKeyboardButton("Апэц", callback_data="option4")

    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("id"))
def callback_id(call):
    import re

    match = re.match(r"id(\d+)", call.data)
    if match:
        test_id = int(match.group(1))
        # Получаем пользователя
        info_user = user_info(call.from_user.id)
        bot.send_message(call.message.chat.id, f"Решаю тест {test_id}")
        submit_test(test_id, info_user[0], info_user[1])
        bot.send_message(call.message.chat.id, "Тест решён")


@bot.callback_query_handler(func=lambda call: True)

def callback(call: types.CallbackQuery):
    info_user = user_info(call.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("начать решать", callback_data="298405")
    markup.add(btn1)#субд

    markup2 = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton("test1", callback_data="321506")
    markup2.add(btn2)#саио

    markup3 = types.InlineKeyboardMarkup(row_width=2)
    btn3 = types.InlineKeyboardButton("начать решать", callback_data="id324848")
    markup3.add(btn3)#омо

    markup4 = types.InlineKeyboardMarkup(row_width=2)
    btn4 = types.InlineKeyboardButton("начать решать", callback_data="305095")
    markup4.add(btn4)#Апэц

    if call.data=="option1":
        bot.send_message(call.message.chat.id, "СУБД:", reply_markup=markup)
    if call.data=="option2":
        bot.send_message(call.message.chat.id, "Саио:", reply_markup=markup2)
    if call.data=="option3":
        bot.send_message(call.message.chat.id, "ОМО:", reply_markup=markup3)
    if call.data=="option4":
        bot.send_message(call.message.chat.id, "АПЭЦ:", reply_markup=markup4)

    # if call.data=="324848":
    #
    #     bot.send_message(call.message.chat.id, "решаю тест")
    #     submit_test(call.data,info_user[0],info_user[1])
    #     bot.send_message(call.message.chat.id, "тест решён")
    #
    # if call.data=="305095":
    #
    #     bot.send_message(call.message.chat.id, "решаю тест")
    #     submit_test(call.data,info_user[0],info_user[1])
    #     bot.send_message(call.message.chat.id, "тест решён")



















bot.infinity_polling()
