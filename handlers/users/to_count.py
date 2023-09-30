import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_button import main_button
from keyboards.inline.drugs_buttons import drugs_list_keyboard, drugs_callback, manipulations_keyboard, \
    back_drug_keyboard
from keyboards.inline.fix_buttons import fix_keyboard, fix_callback
from loader import dp, db_user, bot
from states.fix_state import FixMessage, CalcMessage

from utils.misc import rate_limit
from utils.misc.reset_fsm_state import set_reset_timer
import prettytable as pt

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

    await message.answer("<b>🚩Введіть <u>ВАГУ</u> в кілограмах\n(має бути одне число❗)</b>", reply_markup=main_button)
    await FixMessage.EnterWeight.set()
    logging.info(message.from_user.full_name + " -> pressed [Розрахунки при опіках 🔥]")
    await set_reset_timer(user_id=message.from_user.id, state=state, timeout_seconds=90)


@dp.message_handler(state=FixMessage.EnterWeight)
async def enter_weight(message: types.Message, state: FSMContext):
    if message.text.strip().isdigit():
        await state.update_data(weight=message.text, mention=message.from_user.get_mention())
        await message.answer(f'<b>🚩Введіть кількість <u>ОПІКІВ</u> у відсотках\n(має бути одне число❗)</b>')
        await FixMessage.next()

    else:
        await state.update_data(weight=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть <u>ВАГУ</u> в кілограмах\n(має бути одне число❗)</b>',
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
                f"<b>ВАГА ≈ {round_weight}кг\nОПІКИ ≈ {round_burns}%\nОБ'ЄМ = {mill_per_hour} мл/год\n<u>ШВИДКІСТЬ ВЛИВАННЯ ≈ {drops_per_second:.2f} крапель/секунду</u></b>")
        else:
            mill_per_hour = round_burns * 10
            drops_per_second = (mill_per_hour / 3600) * 20
            await message.answer(
                f"<b>ВАГА ≈ {round_weight}кг\nОПІКИ ≈ {round_burns}%\nОБ'ЄМ = {mill_per_hour} мл/год\n<u>ШВИДКІСТЬ ВЛИВАННЯ ≈ {drops_per_second:.2f} крапель/секунду</u></b>")


    else:
        await state.update_data(text_answer=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть кількість <u>ОПІКІВ</u> у відсотках\n(має бути одне число❗)</b>',
            reply_markup=fix_keyboard)


@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=FixMessage.EnterWeight)
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=FixMessage.EnterBurns)
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

    await call.answer("Дані анульовано!🗑", show_alert=True)


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

"""________________________________________________________________"""
@rate_limit(5, "Розрахунки препаратів 💉")
@dp.message_handler(text="Розрахунки препаратів 💉")
async def drugs_menu(message: types.Message):
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
    logging.info(message.from_user.full_name + " -> pressed [Розрахунки препаратів 💉]")
    await message.answer(text="<b>Виберіть препарат: 💊</b>", reply_markup=drugs_list_keyboard)


@dp.callback_query_handler(drugs_callback.filter(action='interest'))
async def drugs_interest(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    if 'КЕТАМІН' in call.message.text:
        await state.set_state('enter_ketamine')
        await call.message.answer("<b>Введіть %-вість КЕТАМІНУ\n(має бути ціле або число через <u>крапку</u>❗)</b>")
    if 'TXA' in call.message.text:
        await state.set_state('enter_TXA')
        await call.message.answer("<b>Введіть %-вість ТХА\n(має бути ціле або число через <u>крапку</u>❗)</b>")
    if "НАЛОКСОН" in call.message.text:
        await state.set_state('enter_nalokson')
        await call.message.answer("<b>Введіть %-вість НАЛОКСОНУ\n(має бути ціле або число через <u>крапку</u>❗)</b>")
    if "ОНДАСЕТРОН" in call.message.text:
        await state.set_state('enter_ondasetron')
        await call.message.answer("<b>Введіть %-вість ОДАСЕТРОНУ\n(має бути ціле або число через <u>крапку</u>❗)</b>")
    if "Са\u00B2⁺ХЛОРИД" in call.message.text:
        await state.set_state('enter_CaCl')
        await call.message.answer(
            "<b>Введіть %-вість Са\u00B2⁺ХЛОРИДУ\n(має бути ціле або число через <u>крапку</u>❗)</b>")


@dp.callback_query_handler(drugs_callback.filter(action='back_to_drugs'))
async def drugs_manipulations(call: types.CallbackQuery, ):
    await call.message.delete()
    await call.message.answer(text="<b>Виберіть препарат: 💊</b>", reply_markup=drugs_list_keyboard)


@dp.callback_query_handler(fix_callback.filter(action='cancel'), state='Ca_hlukoza')
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state='enter_CaCl')
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state='enter_ondasetron')
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state='enter_nalokson')
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state='enter_ketamine')
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state='enter_TXA')
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=CalcMessage.EnterWight)
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=CalcMessage.EnterPercent)
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

    await call.answer("Дані анульовано!🗑", show_alert=True)

""" Калькулятор препаратів """

@dp.callback_query_handler(drugs_callback.filter(action='calculate'))
async def calculate_drug (call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    await call.message.answer("<b>🚩Введіть <u>%</u>-вість препарату\n(має бути ціле або число через <u>крапку</u>❗)</b>", parse_mode=types.ParseMode.HTML)
    await CalcMessage.EnterPercent.set()




@dp.message_handler(state=CalcMessage.EnterPercent)
async def enter_weight_drug(message: types.Message, state: FSMContext):
    try:
        float_persent = float(message.text.strip())
        await state.update_data(percent=float_persent, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>🚩Введіть  <u>дозу препарату в мг</u> яку потрібго ввести\n(має бути ціле або число через <u>крапку</u>❗)1г-1000мг</b>', parse_mode=types.ParseMode.HTML)
        await CalcMessage.next()
    except ValueError:
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть <u>%</u> препарату\n(має бути ціле або число через <u>крапку</u>❗)</b>',
            reply_markup=fix_keyboard, parse_mode=types.ParseMode.HTML)


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
        await message.answer(f"<b>Доза введення в обємі: {enter_ml} ml</b>", parse_mode=types.ParseMode.HTML)

    except ValueError:
        await state.update_data(text_answer=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть  <u>дозу препарату в мг</u> яку потрібго ввести\n(має бути ціле або число через <u>крапку</u>❗) 1г-1000мг</b>',
            reply_markup=fix_keyboard, parse_mode=types.ParseMode.HTML)






"""KETAMIN"""


@dp.callback_query_handler(drugs_callback.filter(action='ketamine'))
async def ketamine(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення', 'Доза'])
    table.title = 'КЕТАМІН'
    table.align['Введення'] = 'l'
    table.align['Доза'] = 'r'

    data = [
        ('в/в', '20-30 мг'),
        ('в/к', '20-30 мг'),
        ('в/м', '50-100 мг'),
        ('і/н', '50-100 мг'),
    ]
    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>😖знеболення\n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)


@dp.message_handler(state='enter_ketamine')
async def ketamine_calculate(message: types.Message, state: FSMContext):
    try:

        float_persent = float(message.text.strip())
        if float_persent<=0:
            raise ZeroDivisionError()
        mg_ml = float_persent * 1000 / 100
        enter_ml = {'vv_or_vk': f'{20 / mg_ml:.2f}-{30 / mg_ml:.2f} ml',
                    'vm_or_itro_nazal': f'{50 / mg_ml:.2f}-{100 / mg_ml:.2f} ml'}
        await state.finish()
        table = pt.PrettyTable(['Введення', 'Доза'])
        table.title = f'ДОЗА {float_persent}% КЕТАМІНУ в ml'
        table.align['Введення'] = 'l'
        table.align['Доза'] = 'r'

        data = [
            ('в/в', enter_ml['vv_or_vk']),
            ('в/к', enter_ml['vv_or_vk']),
            ('в/м', enter_ml['vm_or_itro_nazal']),
            ('і/н', enter_ml['vm_or_itro_nazal']),
        ]
        for intro, dose in data:
            table.add_row([f'{intro}', f'{dose}'])
        await message.answer(text=f'<pre>😖знеболення\n{table}</pre>',
                             parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)
    except ValueError:
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть <u>%-вість</u> КЕТАМІНУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)
    except ZeroDivisionError:
        print(f'🤦‍️{message.from_user.full_name} тупарь!')
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>🤦‍♂️Зберись, подумай що не так!\nСпробуй ще, введи <u>%-вість</u> КЕТАМІНУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)


"""TXA"""


@dp.callback_query_handler(drugs_callback.filter(action='TXA'))
async def drug_txa(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення', 'Доза'])
    table.title = 'TXA'
    table.align['Введення'] = 'l'
    table.align['Доза'] = 'r'

    data = [
        ('в/в', '2 гр (2000 мг)'),
        ('в/к', '2 гр (2000 мг)'),

    ]
    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>🩸зменшення крововтрати \n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)


@dp.message_handler(state='enter_TXA')
async def TXA_calculate(message: types.Message, state: FSMContext):
    try:
        float_persent = float(message.text.strip())
        if float_persent <= 0:
            raise ZeroDivisionError('🤦‍♂️тупарь!')
        mg_ml = float_persent * 1000 / 100
        enter_ml = {'vv_or_vk': f'{2000 / mg_ml:.2f} ml'
                    }
        await state.finish()
        table = pt.PrettyTable(['Введення', 'Доза'])
        table.title = f'ДОЗА {float_persent}% TXA в ml'
        table.align['Введення'] = 'l'
        table.align['Доза'] = 'r'

        data = [
            ('в/в', enter_ml['vv_or_vk']),
            ('в/к', enter_ml['vv_or_vk']),
        ]
        for intro, dose in data:
            table.add_row([f'{intro}', f'{dose}'])
        await message.answer(text=f'<pre>🩸зменшення крововтрати\n{table}</pre>',
                             parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)
    except ValueError:
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть <u>%-вість</u> TXA\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)
    except ZeroDivisionError:
        print(f'🤦‍️{message.from_user.full_name} тупарь!')
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>🤦‍♂️Зберись, подумай що не так!\nСпробуй ще, введи <u>%-вість</u> TXA\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)


"""НАЛОКСОН"""


@dp.callback_query_handler(drugs_callback.filter(action='nalokson'))
async def nalokson(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення', 'Доза'])
    table.title = 'НАЛОКСОН'
    table.align['Введення'] = 'l'
    table.align['Доза'] = 'r'

    data = [
        ('в/в', '0.4 мг'),
        ('в/к', '0.4 мг'),
        ('в/м', '0.4 мг'),
        ('і/н', '0.4 мг'),

    ]
    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>🧪антидот до опіоїдів\n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)


@dp.message_handler(state='enter_nalokson')
async def nalokson_calculate(message: types.Message, state: FSMContext):
    try:
        float_persent = float(message.text.strip())
        if float_persent <= 0:
            raise ZeroDivisionError('🤦‍♂️тупарь!')
        mg_ml = float_persent * 1000 / 100
        enter_ml = {'vv_or_vk': f'{0.4 / mg_ml:.2f} ml'
                    }
        await state.finish()
        table = pt.PrettyTable(['Введення', 'Доза'])
        table.title = f'ДОЗА {float_persent}% НАЛОКСОНУ в ml'
        table.align['Введення'] = 'l'
        table.align['Доза'] = 'r'

        data = [
            ('в/в', enter_ml['vv_or_vk']),
            ('в/к', enter_ml['vv_or_vk']),
            ('в/м', enter_ml['vv_or_vk']),
            ('і/н', enter_ml['vv_or_vk']),

        ]
        for intro, dose in data:
            table.add_row([f'{intro}', f'{dose}'])
        await message.answer(text=f'<pre>🧪антидот до опіоїдів\n{table}</pre>',
                             parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)
    except ValueError:
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть <u>%-вість</u> НАЛОКСОНУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)
    except ZeroDivisionError:
        print(f'🤦‍️{message.from_user.full_name} тупарь!')
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>🤦‍♂️Зберись, подумай що не так!\nСпробуй ще, введи <u>%-вість</u> НАЛОКСОНУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)


"""ОДАСЕТРОН"""


@dp.callback_query_handler(drugs_callback.filter(action='ondasetron'))
async def ondasetron(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення', 'Доза'])
    table.title = 'ОНДАСЕТРОН'

    table.align['Введення'] = 'l'
    table.align['Доза'] = 'r'
    data = [
        ('в/в', '2мг на 8год'),
        ('в/к', '2мг на 8год'),
        ('в/м', '2мг на 8год'),

    ]
    table.add_row(['Загальна доза', '\u22658мг на добу'])

    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>🤢протиблювотний\n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)


@dp.message_handler(state='enter_ondasetron')
async def ondasetron_calculate(message: types.Message, state: FSMContext):
    try:
        float_persent = float(message.text.strip())
        if float_persent <= 0:
            raise ZeroDivisionError('🤦‍♂️тупарь!')
        mg_ml = float_persent * 1000 / 100
        enter_ml = {'vv_or_vk': f'{2 / mg_ml:.2f} ml'
                    }
        await state.finish()
        table = pt.PrettyTable(['Введення', 'Доза'])
        table.title = f'ДОЗА {float_persent}% ОНДАСЕТРОНУ в ml'
        table.align['Введення'] = 'l'
        table.align['Доза'] = 'r'

        data = [
            ('в/в', f"{enter_ml['vv_or_vk']} на 8год"),
            ('в/к', f"{enter_ml['vv_or_vk']} на 8год"),
            ('в/м', f"{enter_ml['vv_or_vk']} на 8год"),

        ]
        for intro, dose in data:
            table.add_row([f'{intro}', f'{dose}'])
        await message.answer(text=f'<pre>🤢протиблювотний\n{table}</pre>',
                             parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)
    except ValueError:
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть <u>%-вість</u> ОНДАСЕТРОНУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)
    except ZeroDivisionError:
        print(f'🤦‍️{message.from_user.full_name} тупарь!')
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
           f'<b>🤦‍♂️Зберись, подумай що не так!\nСпробуй ще, введи <u>%-вість</u> ОНДАСЕТРОНУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
          reply_markup=fix_keyboard)

"""Са ХЛОРИД"""


@dp.callback_query_handler(drugs_callback.filter(action='CaCl'))
async def ca_cl(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення', 'Доза'])
    table.title = 'Са\u00B2⁺ХЛОРИД'

    table.align['Введення'] = 'l'
    table.align['Доза'] = 'r'
    data = [
        ('в/в', '1 гр (1000мг)'),
        ('в/к', '1 гр (1000мг)'),

    ]

    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>📌«блокатор» цитрату натрія\n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)


@dp.message_handler(state='enter_CaCl')
async def cacl_calculate(message: types.Message, state: FSMContext):
    try:
        float_persent = float(message.text.strip())
        if float_persent <= 0:
            raise ZeroDivisionError('🤦‍♂️тупарь!')
        mg_ml = float_persent * 1000 / 100
        enter_ml = {'vv_or_vk': f'{1000 / mg_ml:.2f} ml'
                    }
        await state.finish()
        table = pt.PrettyTable(['Введення', 'Доза'])
        table.title = f'ДОЗА {float_persent}% Са\u00B2⁺ХЛОРИДУ в ml'
        table.align['Введення'] = 'l'
        table.align['Доза'] = 'r'

        data = [
            ('в/в', f"{enter_ml['vv_or_vk']} "),
            ('в/к', f"{enter_ml['vv_or_vk']} "),

        ]
        for intro, dose in data:
            table.add_row([f'{intro}', f'{dose}'])
        await message.answer(text=f'<pre>📌«блокатор» цитрату натрія\n{table}</pre>',
                             parse_mode=types.ParseMode.HTML, reply_markup=manipulations_keyboard)
    except ValueError:
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
            f'<b>⛔Некоректне значення!\nСпробуй ще, введіть <u>%-вість</u> Са\u00B2⁺ХЛОРИДУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
            reply_markup=fix_keyboard)
    except ZeroDivisionError:
        print(f'🤦‍️{message.from_user.full_name} тупарь!')
        await state.update_data(percent=message.text, mention=message.from_user.get_mention())
        await message.answer(
          f'<b>🤦‍♂️Зберись, подумай що не так!\nСпробуй ще, введи <u>%-вість</u> Са\u00B2⁺ХЛОРИДУ\n(має бути ціле або число через <u>крапку</u>❗</b>)',
          reply_markup=fix_keyboard)


"""Са Глюконат"""


@dp.callback_query_handler(drugs_callback.filter(action='Ca_hlukoza'))
async def ca_hlukoza(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення 10%-го', 'Доза в ml'])
    table.title = 'Са\u00B2⁺ГЛЮКОНАТ'

    table.align['Введення 10%-го'] = 'l'
    table.align['Доза в ml'] = 'r'
    data = [
        ('в/в', '30 ml'),
        ('в/к', '30 ml'),

    ]

    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>📌«блокатор» цитрату натрія\n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=back_drug_keyboard)


"""ФЕНТАНІЛ"""


@dp.callback_query_handler(drugs_callback.filter(action='fentanil'))
async def ca_hlukoza(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення', 'Доза'])
    table.title = 'ФЕНТАНІЛ (льодяник)'

    data = [
        ('1 льодяник', '800 мкг'),

    ]

    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>😖знеболення\n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=back_drug_keyboard)




"""ЕРТАПЕНЕМ"""


@dp.callback_query_handler(drugs_callback.filter(action='ertapenem'))
async def ca_hlukoza(call: types.CallbackQuery, ):
    await call.message.delete()

    table = pt.PrettyTable(['Введення', 'Доза 100%-го'])
    table.title = 'ЕРТАПЕНЕМ'

    data = [
        ('в/в', '1 гр (1000мг)'),
        ('в/к', '1 гр (1000мг)'),
        ('в/м', '1 гр (1000мг)'),

    ]

    for intro, dose in data:
        table.add_row([f'{intro}', f'{dose}'])
    await dp.bot.send_message(chat_id=call.from_user.id, text=f'<pre>💉антибіотик\n{table}</pre>',
                              parse_mode=types.ParseMode.HTML, reply_markup=back_drug_keyboard)
