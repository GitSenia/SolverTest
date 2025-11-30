import telebot

from dotenv import load_dotenv
import os
load_dotenv()

c=os.getenv("TOKEN_BOT")

bot = telebot.TeleBot(c)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот!")

@bot.message_handler(commands=['menu'])
def menu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1=  telebot.types.InlineKeyboardButton(text="Регистрация",callback_data="bt1")

    bt2 = telebot.types.InlineKeyboardButton(text="/start",callback_data="bt2")
    keyboard.add(bt1,bt2)
    bot.send_message(message.chat.id, "Выбери опцию:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "bt1":
        bot.answer_callback_query(call.id, "Вы нажали регистрация")
    if call.data == "bt2":
        bot.send_message(call.message.chat.id, "Нажали решение тестов")




bot.polling()