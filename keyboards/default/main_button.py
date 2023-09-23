from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Розрахунки при опіках 🔥")],
        [KeyboardButton(text="Шпаргалка 📋")],
        [KeyboardButton(text="Розрахунки препаратів 💉%")]

    ], resize_keyboard=True,)
