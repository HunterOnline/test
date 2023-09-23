import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_button import main_button
from keyboards.inline.fix_buttons import fix_keyboard, fix_callback
from loader import dp, db_user, bot
from states.fix_state import FixMessage, CalcMessage

from utils.misc import rate_limit
from utils.misc.reset_fsm_state import set_reset_timer

"""МЕНЮ КНОПОК"""

"""Розрахунки при опіках"""


@rate_limit(5, "Розрахунки при опіках 🔥")
@dp.message_handler(text="Розрахунки при опіках 🔥")
async def calculate_burns(message: types.Message, state: FSMContext):
    name = message.from_user.get_mention()
    user_id = message.from_user.id
    users = db_user.buf_user_data
    if user_id in users:
        logging.info(f"{message.from_user.full_name} -> уже есть БД_S")
    else:
        try:
            db_user.add_user(user_id, name)
            db_user.unload_user_data()
            logging.info(f"{message.from_user.full_name} -> записани в БД")
        except Exception as e:
            print(e)

    await message.answer("🚩Введіть <u>ВАГУ</u> в кілограмах\n(має бути одне число❗)",reply_markup=main_button)
    await FixMessage.EnterWeight.set()
    logging.info(message.from_user.full_name + " -> pressed [Розрахунки при опіках 🔥]")
    await set_reset_timer(user_id=message.from_user.id, state=state, timeout_seconds=90)


@dp.message_handler(state=FixMessage.EnterWeight)
async def enter_weight(message: types.Message, state: FSMContext):
    if message.text.strip().isdigit():
        await state.update_data(weight=message.text, mention=message.from_user.get_mention())
        await message.answer(f'🚩Введіть кількість <u>ОПІКІВ</u> у відсотках\n(має бути одне число❗)')
        await FixMessage.next()

    else:
        await state.update_data(weight=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'⛔Некоректне значення!\nСпробуй ще, введіть <u>ВАГУ</u> в кілограмах\n(має бути одне число❗)',
            reply_markup=fix_keyboard)


@dp.message_handler(state=FixMessage.EnterBurns)
async def enter_weight(message: types.Message, state: FSMContext):
    await state.update_data(burns=message.text, mention=message.from_user.get_mention())
    if message.text.strip().isdigit():
        async with state.proxy() as data:
            weight = int(data.get('weight'))
            burns = int(data.get('burns'))
            await state.finish()
        round_weight = round(weight / 10) * 10
        round_burns = round(burns / 10) * 10
        if weight > 80:
            mill_per_hour = round_burns * 10 + (round_weight - 80) * 10
            drops_per_second = (mill_per_hour / 3600) * 20
            await message.answer(
                f"ВАГА ≈ {round_weight}кг\nОПІКИ ≈ {round_burns}%\nОБ'ЄМ = {mill_per_hour} мл/год\n<u>ШВИДКІСТЬ ВЛИВАННЯ ≈ {drops_per_second:.2f} крапель/секунду</u>")
        else:
            mill_per_hour = round_burns * 10
            drops_per_second = (mill_per_hour / 3600) * 20
            await message.answer(
                f"ВАГА ≈ {round_weight}кг\nОПІКИ ≈ {round_burns}%\nОБ'ЄМ = {mill_per_hour} мл/год\n<u>ШВИДКІСТЬ ВЛИВАННЯ ≈ {drops_per_second:.2f} крапель/секунду</u>")


    else:
        await state.update_data(text_answer=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'⛔Некоректне значення!\nСпробуй ще, введіть кількість <u>ОПІКІВ</u> у відсотках\n(має бути одне число❗)',
            reply_markup=fix_keyboard)


@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=FixMessage.EnterWeight)
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=FixMessage.EnterBurns)
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

    await call.answer("🗑Дані анульовано!", show_alert=True)


"""Шпаргалка"""


@rate_limit(5, "Шпаргалка 📋")
@dp.message_handler(text="Шпаргалка 📋")
async def calculate_burns(message: types.Message):
    name = message.from_user.get_mention()
    user_id = message.from_user.id
    users = db_user.buf_user_data
    if user_id in users:
        logging.info(f"{message.from_user.full_name} -> уже есть БД_S")
    else:
        try:
            db_user.add_user(user_id, name)
            db_user.unload_user_data()
            logging.info(f"{message.from_user.full_name} -> записани в БД")

        except Exception as e:
            print(e)


    await message.answer_document(open("data/препарати.pdf", "rb"), reply_markup=main_button)

    logging.info(message.from_user.full_name + " -> pressed [Шпаргалка 📋]")


"""Розрахунки препаратів 💉%"""


@rate_limit(5, "Розрахунки препаратів 💉%")
@dp.message_handler(text="Розрахунки препаратів 💉%")
async def calculate_drug(message: types.Message, state: FSMContext):
    name = message.from_user.get_mention()
    user_id = message.from_user.id
    users = db_user.buf_user_data
    if user_id in users:
        logging.info(f"{message.from_user.full_name} -> уже есть БД_S")
    else:
        try:
            db_user.add_user(user_id, name)
            db_user.unload_user_data()
            logging.info(f"{message.from_user.full_name} -> записани в БД")

        except Exception as e:
            print(e)

    await message.answer(
        "☝ Дані розрахунки актуальні не для всіх препаратів, вміст <u>Кальция глюконат</u> обраховується по іншому!\n"
        "Актуально: <u>Кетамін, Налоксон, Ондансетрон, Кальція хлорид, ТХА</u>", reply_markup=main_button)
    await message.answer("🚩Введіть <u>%</u>-вість препарату\n(має бути ціле або число через <u>крапку</u>❗)")
    await CalcMessage.EnterPercent.set()
    logging.info(message.from_user.full_name + " -> pressed [Розрахунки препаратів 💉%]")


@dp.message_handler(state=CalcMessage.EnterPercent)
async def enter_weight_drug(message: types.Message, state: FSMContext):
    try:
        float_persent = float(message.text.strip())
        await state.update_data(percent=float_persent, mention=message.from_user.get_mention())
        await message.answer(
            f'🚩Введіть  <u>дозу препарату в мг</u> яку потрібго ввести\n(має бути ціле або число через <u>крапку</u>❗)1г-1000мг')
        await CalcMessage.next()
    except ValueError:
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'⛔Некоректне значення!\nСпробуй ще, введіть <u>%</u> препарату\n(має бути ціле або число через <u>крапку</u>❗)',
            reply_markup=fix_keyboard)


@dp.message_handler(state=CalcMessage.EnterWight)
async def enter_weight(message: types.Message, state: FSMContext):
    await state.update_data(wight=message.text, mention=message.from_user.get_mention())
    try:
        async with state.proxy() as data:
            percent = float(data.get('percent'))
            wight = float(data.get('wight'))
            await state.finish()
        mg_ml = percent * 1000 / 100
        enter_ml = wight / mg_ml
        await message.answer(f"Доза введення в обємі: {enter_ml} ml")

    except ValueError:
        await state.update_data(text_answer=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'⛔Некоректне значення!\nСпробуй ще, введіть  <u>дозу препарату в мг</u> яку потрібго ввести\n(має бути ціле або число через <u>крапку</u>❗) 1г-1000мг',
            reply_markup=fix_keyboard)


@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=CalcMessage.EnterPercent)
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=CalcMessage.EnterPercent)
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

    await call.answer("🗑Дані анульовано!", show_alert=True)
