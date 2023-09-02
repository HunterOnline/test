import asyncio

from aiogram.dispatcher import FSMContext

from loader import dp




# Функція для скидання стану користувача
async def reset_user_state(user_id, state: FSMContext):
    await state.finish()  # Скидання стану користувача
    # await dp.bot.send_message(chat_id=user_id, text='⏱ ліміт очікування вичерпано...', )
    # Додайте інші дії, які ви хочете виконати після скидання стану




# Функція для встановлення таймера на скидання стану користувача
async def set_reset_timer(user_id, state: FSMContext, timeout_seconds):
    await asyncio.sleep(timeout_seconds)  # Зачекайте вказану кількість секунд
    await reset_user_state(user_id, state)  # Скинути стан користувача


