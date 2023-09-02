from aiogram.dispatcher.filters.state import StatesGroup, State


class FixMessage(StatesGroup):
    EnterWeight = State()
    EnterBurns = State()


class CalcMessage(StatesGroup):
    EnterPercent = State()
    EnterWight = State()
