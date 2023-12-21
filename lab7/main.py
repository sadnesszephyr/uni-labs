import telebot
from telebot import types
import psycopg2
from datetime import datetime

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname='lab8',
    user='postgres',
    password='',
    host='localhost',
    port=5432
)

# Создание экземпляра бота
bot = telebot.TeleBot('')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    current_week = datetime.today().isocalendar().week
    # Отправка приветственного сообщения
    bot.reply_to(message, current_week % 2)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
    for day in days:
        markup.add(types.KeyboardButton(day))
    markup.add(types.KeyboardButton('Расписание на текущую неделю'))
    markup.add(types.KeyboardButton('Расписание на следующую неделю'))
    bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=markup)


# Обработчик команды /week
@bot.message_handler(commands=['week'])
def handle_week(message):
    # Отправка информации о текущей неделе
    bot.reply_to(message, 'Текущая неделя - верхняя/нижняя')

# Обработчик команды /mtuci
@bot.message_handler(commands=['mtuci'])
def handle_mtuci(message):
    # Отправка ссылки на официальный сайт МТУСИ
    bot.reply_to(message, 'Ссылка на официальный сайт МТУСИ: https://mtuci.ru/')

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    # Отправка информации о боте и доступных командах
    help_message = '''Я бот с расписанием для группы.

Доступные команды:
/start - начать общение с ботом
/week - узнать текущую неделю
/mtuci - получить ссылку на официальный сайт МТУСИ
/help - вывести список доступных команд и их описание
'''
    bot.reply_to(message, help_message)

# Обработчик неизвестных команд и сообщений
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    # Отправка сообщения об ошибке
    bot.reply_to(message, 'Извините, я Вас не понял.')

# Запуск бота
bot.polling()