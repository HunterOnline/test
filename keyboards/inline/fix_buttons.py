from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

fix_callback = CallbackData("fix_mess", "action")

fix_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        
        [
            InlineKeyboardButton(text="Вийти", callback_data=fix_callback.new(action='cancel'))
        ]

    ]
)