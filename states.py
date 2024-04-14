from telebot.handler_backends import StatesGroup, State


class UserInputState(StatesGroup):
    start_filter = State()   # стартовая опция
    age_filter = State()  # ограничение участников по возрасту
    min_members_filter = State()
    max_members_filter = State()
    members_filter = State()  # количество участников мероприятия
    scary_filter = State()  # уровень "сложности"
    rating_filter = State()  # рейтинг
    types_filter = State()  # фильтр по типу мероприятия
    middle_rez_1 = State()
    middle_rez_2 = State()
    middle_rez_3 = State()
    middle_rez_4 = State()
    middle_rez_5 = State()
