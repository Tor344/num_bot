from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from  aiogram import Bot
from app.json_red import update_text_in_json,update_photo_in_json
from datetime import datetime


import app.SQLite as db
import app.request as req

import app.button as butten
router = Router()

class Reg_db(StatesGroup):
    birth = State()
    name = State()

class Date(StatesGroup):
    birth = State()

class Consol(StatesGroup):
    change = State()
    photo = State()
    text = State()

@router.message(Command('start'))
async def start(message: Message,state:FSMContext,bot: Bot):
    reg = await db.examination_user(message.from_user.id)
    user_channel_status = await bot.get_chat_member(chat_id='@num_channel', user_id=message.from_user.id)
    if not user_channel_status.status in ["member", "administrator", "creator"]:
        await message.answer("""Описание с подпиской @num_channel
                """, reply_markup=butten.subscription_keyboard)
    elif not reg:
        await state.set_state(Reg_db.birth)
        await db.regist_user(message.from_user.id)
        await message.answer("Введите день рождения в формате (20-10-2021)", reply_markup=None)
    else:
        await message.answer("Главный текст другой текст", reply_markup=butten.main_keyboard)


@router.callback_query(F.data == "examination")
async def main_panel(call: CallbackQuery,bot:Bot,state:FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@num_channel', user_id=call.from_user.id)
    reg = await db.examination_user(call.from_user.id)
    if not user_channel_status.status in ["member", "administrator", "creator"]:
        await call.message.edit_text("""Вы не подписаны, подпишитесь  @num_channel
                """, reply_markup=butten.subscription_keyboard)
    elif not reg:
        await db.regist_user(call.from_user.id)
        await state.set_state(Reg_db.birth)
        await call.message.answer("Введите день рождения в формате (20-10-2021)", reply_markup=None)

    else:
        await call.message.edit_text("Главный текст другой текст", reply_markup=butten.main_keyboard)


@router.callback_query(F.data == "forecast")
async def main_panel(call: CallbackQuery,bot:Bot):
    user_channel_status = await bot.get_chat_member(chat_id='@num_channel', user_id=call.from_user.id)
    if not user_channel_status.status in ["member", "administrator", "creator"]:
        await call.message.edit_text("""Вы не подписаны, подпишитесь  @num_channel
                    """, reply_markup=butten.subscription_keyboard)
    else:
        now = datetime.now()
        today = str(now.date())
        date = list(await db.giv_data(call.from_user.id))[1]
        result = req.validate(int(date[0:2]),int(date[3:5]),int(today[8:10]),int(today[5:7]),int(today[0:4]))
        await call.message.delete()
        await call.message.answer_photo(result[2],caption="сегодняшний прогноз")
        await call.message.answer(f"Ваш Нумерологический код этого дня: {result[0]}\n{result[1]}",reply_markup=butten.beck_keyboard)


@router.message(Reg_db.birth)
async def main_panel(message: Message,state:FSMContext):
    birth = message.text.split("-")
    if not req.is_valid_date(int(birth[0]),int(birth[1]),int(birth[2])):
        await message.answer("Вы неправильно заполнили дату рождения, попробуйте еще раз")
    else:
        await state.update_data(birth=message.text)
        await state.set_state(Reg_db.name)
        await message.answer("Напишите свое имя")


@router.message(Reg_db.name)
async def main_panel(message: Message,state:FSMContext):
    data = await state.get_data()
    await db.get_data(message.from_user.id,data["birth"], message.text)
    await state.clear()
    await message.answer("Главный текст другой текст", reply_markup=butten.main_keyboard)


@router.callback_query(F.data == "choice_date")
async def main_panel(call: CallbackQuery,state: FSMContext,bot:Bot):
    user_channel_status = await bot.get_chat_member(chat_id='@num_channel', user_id=call.from_user.id)
    if not user_channel_status.status in ["member", "administrator", "creator"]:
        await call.message.edit_text("""Вы не подписаны, подпишитесь  @num_channel
                    """, reply_markup=butten.subscription_keyboard)
    else:
        await state.set_state(Date.birth)
        await call.message.edit_text("Введите дату в формате (20-10-2021)", reply_markup=None)


@router.message(Date.birth)
async def main_panel(message: Message,state:FSMContext):
    birth = message.text.split("-")
    if not req.is_valid_date(int(birth[0]), int(birth[1]), int(birth[2])):
        await message.answer("Вы неправильно заполнили дату рождения, попробуйте еще раз")
    else:
        await state.clear()
        date = list(await db.giv_data(message.from_user.id))[1]
        result = req.validate(int(date[0:2]), int(date[3:5]), int(birth[0]), int(birth[1]), int(birth[2]))
        await message.answer_photo(result[2],caption=f"Прогноз на {message.text}")
        await message.answer(f"Ваш Нумерологический код этого дня: {result[0]}\n{result[1]}",
                                     reply_markup=butten.beck_keyboard)


@router.callback_query(F.data == "subscription_date")
async def main_panel(call: CallbackQuery,bot:Bot):
    user_channel_status = await bot.get_chat_member(chat_id='@num_channel', user_id=call.from_user.id)
    if not user_channel_status.status in ["member", "administrator", "creator"]:
        await call.message.edit_text("""Вы не подписаны, подпишитесь  @num_channel
                    """, reply_markup=butten.subscription_keyboard)
    else:
        await db.up_flaf(call.from_user.id,1)
        await call.message.edit_text("Вы подписались", reply_markup=butten.un_newsletter_keyboard)


@router.callback_query(F.data == "unsubscribe")
async def main_panel(call: CallbackQuery,bot:Bot):
    user_channel_status = await bot.get_chat_member(chat_id='@num_channel', user_id=call.from_user.id)
    if not user_channel_status.status in ["member", "administrator", "creator"]:
        await call.message.edit_text("""Вы не подписаны, подпишитесь  @num_channel
                    """, reply_markup=butten.newsletter_keyboard)
    else:
        await db.up_flaf(call.from_user.id,0)
        await call.message.edit_text("Вы отписались", reply_markup=butten.newsletter_keyboard)

@router.callback_query(F.data == "beck")
async def main_panel(call: CallbackQuery):
    # messages = await call.message.chat.get_history(limit=2)  # Получаем последние 2 сообщения
    # if messages.photo:
    #     await messages[1].delete()  # Удаляем предпоследнее сообщение
    await call.message.delete()
    await call.message.answer("Главный текст другой текст", reply_markup=butten.main_keyboard)

@router.message(Command("console"))
async def console(message: Message, state:FSMContext):
    await message.answer("Ведите число от 1-9 над готорым будет проводится операция")
    await state.set_state(Consol.change)


@router.message(F.text,Consol.change)
async def ph_or_text(message:Message,state: FSMContext):
    if int(message.text) < 1 or int(message.text) > 9:
        await message.answer("такого числа нет, попробуйте еще")
    else:
        await state.update_data(num=int(message.text))
        await message.answer("Выберите данные, которые хотите измненить",reply_markup=butten.ph_or_text_keyboard)
        await state.set_state(Consol.change)


@router.callback_query(F.data.in_(["photo","text"]))
async def main_panel(call: CallbackQuery,state:FSMContext):
    if call.data == "photo":
        await state.set_state(Consol.photo)
        await call.message.edit_text("Пришилте фотографию")
    elif call.data == "text":
        await state.set_state(Consol.text)
        await call.message.edit_text("Пришилте текст Enter заменив на\\n")


@router.message(F.text, Consol.text)
async def main_panel(message: Message,state:FSMContext):
    text = message.text
    data = await state.get_data()
    update_text_in_json('data.json',data["num"],text)
    await state.clear()


@router.message(F.photo, Consol.photo)
async def main_panel(message: Message, state: FSMContext):

    photo = message.photo[-1]  # Берем наибольшее качество
    file_id = photo.file_id
    data = await state.get_data()
    update_photo_in_json('data.json',data["num"],file_id)
    await state.clear()

# @router.message(F.photo)
# async def handle_photo(message: types.Message):
#     # Получаем файл фотографии
#     photo = message.photo[-1]  # Берем наибольшее качество
#     file_id = photo.file_id
#     await message.answer(f"{file_id}")