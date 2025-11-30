import telebot
from dotenv import load_dotenv
import os
load_dotenv()

c=os.getenv("TOKEN_BOT")

bot = telebot.TeleBot(c)


