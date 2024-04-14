import telebot as telebot
import time
from loguru import logger
from telebot import types
from telebot.types import Message, BotCommand

from my_emojize import *
from select_kvest import show_kvest_info
from sqlquery import read_data_age, read_data_members, read_data_scary, read_data_rating, read_data_type, get_url_query
from states import UserInputState

BOT_TOKEN = '6086834720:AAF-xptg9XdY-gjzWVBOpcux89MWpIbnnyQ'
bot = telebot.TeleBot(token=BOT_TOKEN)


DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Помощь по командам бота")
)

def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS])


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))


@bot.message_handler(commands=['start'])
@logger.catch
def bot_start(message: Message) -> None:
    """
    Функция, реагирующая на команду 'start'. Выводит приветственное сообщение.
    :param message: сообщение Telegram
    """
    logger.info('Начнем заполнять информацию')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')
    markup.row(item1, item2)
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, f'👋 Привет!\n'
                                      f'Мы рады видеть тебя в этом чат боте\n'
                                      f'Здесь ты можешь выбрать любой квест по вкусу\n'
                                      f'Если хочешь перейти на сайт, то нажми на ссылку ниже\n'
                                      f'https://mir-kvestov.ru')
    bot.send_message(message.chat.id, "Начнем?", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == 'Новое заполнение' or m.text == 'Да' and m.content_type == 'text')
@logger.catch
def start_yes(m: Message) -> None:
    """
    Функция, предоставляющая пользователю выбор ограничения по возрасту.
    Выводит кнопки с выбором возрастного ограничения
    :param m: сообщение Telegram
    :return: None
    """
    logger.info('Сортировка по возрасту')
    markup_age = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item11 = types.KeyboardButton(f"{age_emoji[0]} 6+")
    item21 = types.KeyboardButton(f"{age_emoji[1]} 7+")
    item31 = types.KeyboardButton(f"{age_emoji[2]} 8+")
    item41 = types.KeyboardButton(f"{age_emoji[3]} 10+")
    item51 = types.KeyboardButton(f"{age_emoji[4]} 12+")
    item61 = types.KeyboardButton(f"{age_emoji[5]} 14+")
    item71 = types.KeyboardButton(f"{age_emoji[6]} 16+")
    item81 = types.KeyboardButton(f"{age_emoji[7]} 18+")
    markup_age.row(item11, item21, item31)
    markup_age.row(item41, item51, item61)
    markup_age.row(item71, item81)
    bot.send_message(m.chat.id, "Выберите минимальный возраст среди участников", reply_markup=markup_age)


@bot.message_handler(func=lambda m: m.text == 'Нет' and m.content_type == 'text')
@logger.catch
def start_no(m: Message) -> None:
    bot.send_message(m.chat.id, "На нашем сайте ты можешь выбрать любой квест\n"
                                "https://mir-kvestov.ru")


@bot.message_handler(func=lambda m: m.text[:1] in age_emoji)
@logger.catch
def choice_age(m: Message):
    logger.info(f'Пользователь ввел ограничение по возрасту {m.text[1:]}')
    bot.set_state(m.chat.id, UserInputState.age_filter)
    with bot.retrieve_data(m.chat.id) as data:
        data.clear()
        data['age_filter'] = int(m.text[2:-1])
        data['middle_rez_1'] = read_data_age(int(m.text[2:-1]))
        logger.info(f"Результат фильтра {data['middle_rez_1']} вариантов")
    logger.info('Сортировка по количеству участников')
    markup_num = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    num1 = types.KeyboardButton(f"{num_emoji[0]} от 1 до 10")
    num2 = types.KeyboardButton(f"{num_emoji[1]} от 2 до 10")
    num3 = types.KeyboardButton(f"{num_emoji[2]} от 10 до 20")
    num4 = types.KeyboardButton(f"{num_emoji[3]} от 20 до 100")
    markup_num.row(num1, num2)
    markup_num.row(num3, num4)
    bot.send_message(m.chat.id, 'Введите максимальное число участников', reply_markup=markup_num)


@bot.message_handler(func=lambda m: m.text[:1] in num_emoji)
@logger.catch
def choice_members(m):
    logger.info(f'Пользователь ввел количество участников {m.text}')
    with bot.retrieve_data(m.chat.id) as data:
        if len(m.text[5:]) == 7:
            data['min_members_filter'] = int(m.text[5:6])
            data['max_members_filter'] = int(m.text[10:])
        else:
            data['min_members_filter'] = int(m.text[5:8])
            data['max_members_filter'] = int(m.text[11:])
        data['middle_rez_2'] = read_data_members(data['middle_rez_1'], data['min_members_filter'], data['max_members_filter'])
        if len(data['middle_rez_2']) == 0:
            bot.send_message(m.chat.id, "По Вашему запросу ничего не найдено. Попробуйте снова")
            bot.send_message(m.chat.id, '/start')
        logger.info(f"Результат фильтра {data['middle_rez_2']}")
    logger.info('Сортировка по уровню scary')
    markup_scary = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item12 = types.KeyboardButton(f"{scary_emoji[0]} 0+")
    item22 = types.KeyboardButton(f"{scary_emoji[1]} 1+")
    item33 = types.KeyboardButton(f"{scary_emoji[2]} 3+")
    markup_scary.row(item12, item22, item33)
    bot.send_message(m.chat.id, "Выберите уровень реалистичности", reply_markup=markup_scary)


@bot.message_handler(func=lambda m: m.text[:1] in scary_emoji)
@logger.catch
def choice_scary(m):
    logger.info(f'Пользователь ввел уровень scary {m.text}')
    with bot.retrieve_data(m.chat.id) as data:
        data['scary_filter'] = int(m.text[2:3])
        data['middle_rez_3'] = read_data_scary(data['middle_rez_2'], data['scary_filter'])
        if len(data['middle_rez_3']) == 0:
            bot.send_message(m.chat.id, "По Вашему запросу ничего не найдено. Попробуйте снова")
            bot.send_message(m.chat.id, '/start')
        logger.info(f"Результат фильтра {data['middle_rez_3']}")
    markup_rating = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item40 = types.KeyboardButton(f"{rate_emoji[0]} без рейтинга")
    item41 = types.KeyboardButton(f"{rate_emoji[1]} 7")
    item42 = types.KeyboardButton(f"{rate_emoji[2]} 8")
    item43 = types.KeyboardButton(f"{rate_emoji[3]} 9")
    item44 = types.KeyboardButton(f"{rate_emoji[4]} 10")
    markup_rating.row(item41, item42)
    markup_rating.row(item43, item44)
    markup_rating.row(item40)
    logger.info('Сортировка по рейтингу')
    bot.send_message(m.chat.id, "Выберите рейтинг мероприятия", reply_markup=markup_rating)


@bot.message_handler(func=lambda m: m.text[:1] in rate_emoji)
@logger.catch
def rating(m):
    logger.info(f'Пользователь ввел рейтинг {m.text}')
    with bot.retrieve_data(m.chat.id) as data:
        if m.text[1:].isdigit():
            data['rating_filter'] = m.text[1:]
        else:
            data['rating_filter'] = 0
        data['middle_rez_4'] = read_data_rating(data['middle_rez_3'], data['rating_filter'])
        if len(data['middle_rez_4']) == 0:
            bot.send_message(m.chat.id, "По Вашему запросу ничего не найдено. Попробуйте снова")
            bot.send_message(m.chat.id, '/start')
        logger.info(f"Результат фильтра {data['middle_rez_4']}")
    logger.info('Сортировка по типу мероприятия')
    markup_type = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item51 = types.KeyboardButton(f"{type_emoji[0]} Перформанс")
    item52 = types.KeyboardButton(f"{type_emoji[1]} Квест")
    item53 = types.KeyboardButton(f"{type_emoji[2]} Ролевой квест")
    item54 = types.KeyboardButton(f"{type_emoji[3]} VR-квест")
    item55 = types.KeyboardButton(f"{type_emoji[4]} Квест-анимация")
    item56 = types.KeyboardButton(f"{type_emoji[5]} Онлайн-квест")
    item57 = types.KeyboardButton(f"{type_emoji[6]} Городской квест")
    item58 = types.KeyboardButton(f"{type_emoji[7]} Экшн-игра")
    item59 = types.KeyboardButton(f"{type_emoji[8]} Квиз")
    markup_type.row(item51, item52)
    markup_type.row(item53, item54)
    markup_type.row(item55, item56)
    markup_type.row(item57, item58, item59)
    bot.send_message(m.chat.id, "Выберите тип мероприятия", reply_markup=markup_type)


@bot.message_handler(func=lambda m: m.text[:1] in type_emoji)
@logger.catch
def typies(m) -> None:
    logger.info(f'Пользователь ввел тип мероприятия {m.text}')
    with bot.retrieve_data(m.chat.id) as data:
        data['types_filter'] = m.text[2:]
        data['middle_rez_5'] = read_data_type(data['middle_rez_4'], data['types_filter'])
        if len(data['middle_rez_5']) == 0:
            bot.send_message(m.chat.id, "По Вашему запросу ничего не найдено. Попробуйте снова")
            bot.send_message(m.chat.id, '/start')
        logger.info(f"Результат фильтра {data['middle_rez_5']}")
    bot.send_message(m.chat.id, "Вы ввели все необходимые данные для поиска")
    del_keyboard = types.ReplyKeyboardRemove()
    bot.send_message(m.chat.id, "Проверьте Ваш запрос:\n"
                                f"Минимальный возраст участников: {data['age_filter']}\n"
                                f"Максимальное количество участников мероприятия: {data['max_members_filter']}\n"
                                f"Уровень сложности: {data['scary_filter']}\n"
                                f"Рейтинг: {data['rating_filter']}\n"
                                f"Тип мероприятия: {data['types_filter']}", reply_markup=del_keyboard)
    markup_rezult = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item61 = types.KeyboardButton('Продолжить')
    item62 = types.KeyboardButton('Новое заполнение')
    markup_rezult.row(item61, item62)
    bot.send_message(m.chat.id, "Если все правильно то нажмите кнопку 'Продолжить'."
                                "Если нужно изменить запрос, то нажмите 'Новое заполнение'", reply_markup=markup_rezult)
    logger.info('Первый модуль завершен')


@bot.message_handler(func=lambda m: m.text == "Продолжить")
@logger.catch
def make_query(m):
    bot.send_message(m.chat.id, 'Обрабатываем ваш запрос', reply_markup=types.ReplyKeyboardRemove())
    time.sleep(3)
    logger.info(f'Посылаем запрос к базе данных для фильтрации и вывода результата')
    with bot.retrieve_data(m.chat.id) as data:
        records = data['middle_rez_5']
        counter = 1
        for i in list(records):
            if counter <= 3:
                # bot.send_message(m.chat.id, get_url_query(i[0])[0] + show_kvest_info(i[0])[0])
                bot.send_message(m.chat.id, *get_url_query(i[0])[0])
                bot.send_message(m.chat.id, show_kvest_info(*get_url_query(i[0])[0]))
                counter += 1
            else:
                break


@bot.message_handler(func=lambda m: m.text == "Новое заполнение")
@logger.catch
def return_start(m):
    bot.send_message(m.chat.id, 'Очищаем запрос ...')
    time.sleep(2)
    logger.info(f'Возвращаемся к началу ввода данных')
    bot_start()



if __name__ == '__main__':
    set_default_commands(bot)
    bot.infinity_polling()
