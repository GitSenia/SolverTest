import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message,InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re

from src.bot_tg import config as c
from src.tests.pars import submit_test
from src.db.DB_f import user_info,insert_user,update_info
ADMIN_IDS = [945376146, 5778651984]
bot=Bot(c.TOKEN_BOT)

dp=Dispatcher()

class Form(StatesGroup):
    user_name=State()
    password=State()

class Test(StatesGroup):
    id_test=State()
    start=State()

class Admin(StatesGroup):
    username=State()



@dp.message(Command("start"))
async def registration(message: Message):
    await bot.send_message(message.chat.id,"Привет!")



@dp.message(Command("registration"))
async def registration(message: Message,state: FSMContext):
    await state.set_state(Form.user_name)
    await bot.send_message(message.chat.id,"введите логин от сэо")

@dp.message(Form.user_name)
async def get_username(message: Message,state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.password)
    await bot.send_message(message.chat.id, "введите пароль от сэо")

@dp.message(Form.password)
async def get_username(message: Message,state: FSMContext):
    await state.update_data(password=message.text)
    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(tg_name=message.from_user.username)
    data= await state.get_data()

    if await insert_user(data['username'], data['password'],data["tg_id"],data["tg_name"]):
        await bot.send_message(message.chat.id, "Регистрация прошла успешно")
    else:
        await bot.send_message(message.chat.id, "Вы уже зарегистрированы")
    await state.clear()


@dp.message(Command("test"))
async def test(message: Message):

    btn1 = InlineKeyboardButton(text="СУБД", callback_data="option1")
    btn2 = InlineKeyboardButton(text="САИО", callback_data="option2")
    btn3 = InlineKeyboardButton(text="ОМО", callback_data="option3")
    btn4 = InlineKeyboardButton(text="Апэц", callback_data="option4")
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1,btn2,btn3,btn4]])
    await bot.send_message(message.chat.id,text="Выберете тест",reply_markup=markup)


@dp.message(Command("testid"))
async def test_id(message: Message,state: FSMContext):
    await bot.send_message(message.chat.id,text="Введите id теста")
    await state.set_state(Test.id_test)

@dp.message(Command("admin"))
async def admin(message: Message,state: FSMContext):
    await bot.send_message(message.chat.id, text="Введите пользователя")
    await state.set_state(Admin.username)



@dp.message(Admin.username)
async def get_username(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await bot.send_message(message.chat.id, text="У вас нет прав доступа")
    else:
        try:
            if await update_info(message.text):
                await bot.send_message(message.chat.id, text="пользователь обновлён")
            else:
                await bot.send_message(message.chat.id, text="такого пользователя нет")
        except Exception as e:
            await bot.send_message(message.chat.id, text=f"какая-то ошибка{e}")
    await state.clear()





@dp.message(Test.id_test)
async def id_test(message: Message, state: FSMContext):
    await state.update_data(id_test=message.text)
    data = await state.get_data()
    btn2 = InlineKeyboardButton(text="начать решать", callback_data=f"id{data['id_test']}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn2]])
    await bot.send_message(message.chat.id,text=f"Номер теста {data['id_test']}",reply_markup=markup)
    await state.clear()




@dp.callback_query(F.data.regexp(r"option"))
async def callback(call: CallbackQuery):

    btn1 = InlineKeyboardButton(text="начать решать", callback_data="id298405")
    markup1 = InlineKeyboardMarkup(inline_keyboard=[[btn1]])# субд

    btn2 = InlineKeyboardButton(text="начать решать", callback_data="id321554")
    markup2 = InlineKeyboardMarkup(inline_keyboard=[[btn2]]) #саио


    btn3 = InlineKeyboardButton(text="начать решать", callback_data="id324848")
    markup3 = InlineKeyboardMarkup(inline_keyboard=[[btn3]]) #омо

    btn4 = InlineKeyboardButton(text="начать решать", callback_data="id305095")
    markup4 = InlineKeyboardMarkup(inline_keyboard=[[btn4]]) #Апэц

    if call.data=="option1":
       await bot.send_message(call.message.chat.id, "СУБД:", reply_markup=markup1)
    if call.data=="option2":
        await bot.send_message(call.message.chat.id, "Саио:", reply_markup=markup2)
    if call.data=="option3":
        await bot.send_message(call.message.chat.id, "ОМО:", reply_markup=markup3)
    if call.data=="option4":
        await bot.send_message(call.message.chat.id, "АПЭЦ:", reply_markup=markup4)


@dp.callback_query(F.data.regexp(r"^id(\d+)$"))
async def solve(call: CallbackQuery):
    match = re.match(r"^id(\d+)$", call.data)
    test_id = int(match.group(1))

    info_user= await user_info(call.from_user.id)
    if info_user is None:
        await bot.send_message(call.message.chat.id,text="Пользователь не зарегистрирован или не оплачено")
    else:
        await bot.send_message(call.message.chat.id,text="Начинаю решать...")
        try:
            await asyncio.to_thread(submit_test,test_id,info_user[0],info_user[1])
            await bot.send_message(call.message.chat.id, text="тест решён...")
        except Exception as e:
            logging.error(f"Ошибка при решении теста: {e} у user:{info_user[2]} ")
            await bot.send_message(call.message.chat.id, text="ошибка при решении теста")






async def main():
    try:
        logging.info("Бот запускается...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
