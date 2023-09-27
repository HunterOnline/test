from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

drugs_callback = CallbackData("menu_mess", "action")

drugs_list_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="КЕТАМІН", callback_data=drugs_callback.new(action='ketamine'))],
        [InlineKeyboardButton(text="TXA", callback_data=drugs_callback.new(action='TXA'))],
        [InlineKeyboardButton(text="НАЛОКСОН", callback_data=drugs_callback.new(action='nalokson'))],
        [InlineKeyboardButton(text="ОНДАСЕТРОН", callback_data=drugs_callback.new(action='ondasetron'))],
[InlineKeyboardButton(text="Са\u00B2⁺ХЛОРИД", callback_data=drugs_callback.new(action='CaCl'))],
[InlineKeyboardButton(text="Са\u00B2⁺ГЛЮКОНАТ", callback_data=drugs_callback.new(action='Ca_hlukoza'))],
[InlineKeyboardButton(text="ФЕНТАНІЛ (льодяник)", callback_data=drugs_callback.new(action='fentanil'))],
[InlineKeyboardButton(text="ЕРТАПЕНЕМ", callback_data=drugs_callback.new(action='ertapenem'))],
[InlineKeyboardButton(text="Калькулятор", callback_data=drugs_callback.new(action='calculate'))],


    ]
)


manipulations_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Порахувати в ml", callback_data=drugs_callback.new(action='interest'))],
        [InlineKeyboardButton(text="⬅ до препаратів", callback_data=drugs_callback.new(action='back_to_drugs'))]
                     ])



back_drug_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text="⬅ до препаратів", callback_data=drugs_callback.new(action='back_to_drugs'))]
                     ])