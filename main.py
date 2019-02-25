import telebot
import config
import schedule
import time
from telebot import apihelper
from sqlalchemy import create_engine, select
from database import place

# На всякий случай: '\n'.join(map(str, r))

# токен бота
bot = telebot.TeleBot(config.token)

# Настройка прокси
apihelper.proxy = {"https": "socks5://132.145.36.9:1080"}

# Присоединение к базе данных
engine = create_engine('postgresql://127.0.0.1:5432/mydb', echo=True)


# Простой лог чтобы видеть что происходит в боте при взаимодействии с пользователем, в самом терминале
def log(message, answer):
    print("\n ------------------------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \n Текст - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print(answer)


# Приветственное сообщение
@bot.message_handler(commands=['start'])
def send_message(message):
    answer = "Здравствуйте я Бот-помощник \nВведите команду для получения информации о месте проведения собеседования "\
             "\nНапример: /radius"
    bot.send_message(message.chat.id, answer)
    log(message, answer)


# Команда вывода всех команд с подробностями
@bot.message_handler(commands=['help'])
def handle_help(message):
    answer = "Список команд:" \
             "\n/start - приветствие" \
             "\n/radius - информация о компании ООО Радиус" \
             "\n/kb - информация о кампании Красное и Белое" \
             "\n/remind - настройка ежедневного напоминания. \nПример: /remind число(01.01.2019) время(13:00) время в "\
             "\nкоторое будет приходить ежедневное напоминание(10:00) "
    bot.send_message(message.chat.id, answer)
    log(message, answer)


# Команда на вывод информации о компании Радиус
# noinspection PyStringFormat
@bot.message_handler(commands=['radius'])
def find_info(message):
    raw = message.text
    if raw != str('/radius'):
        bot.send_message(message.chat.id, "Упс, похоже вы ошиблись")
    elif raw == str('/radius'):
        select_stmt = select([place.name, place.phone, place.address, place.map, place.panorama]). \
            where(place.id == '1')
        result = engine.execute(select_stmt)
        for r in result:
            bot.send_message(message.chat.id, "Название организации: {}"
                                              "\nКонтактный номер телефона: {} "
                                              "\nТочный адрес: {} "
                                              "\nСсылка на навигатор: {} "
                                              "\nСсылка на панораму(работает только на ПК): {}".format(r.name,
                                                                                                       r.phone,
                                                                                                       r.address,
                                                                                                       r.map,
                                                                                                       r.panorama))
            log(message, r)


# Команда на вывод информации о компании Красное и Белое
# noinspection PyStringFormat
@bot.message_handler(['kb'])
def find_info(message):
    raw = message.text
    if raw != str('/kb'):
        bot.send_message(message.chat.id, "Упс, похоже вы ошиблись")
    elif raw == str('/kb'):
        select_stmt = select([place.name, place.phone, place.address, place.map, place.panorama]). \
            where(place.id == '2')
        result = engine.execute(select_stmt)
        for r in result:
            bot.send_message(message.chat.id, "Название организации: {}"
                                              "\nКонтактный номер телефона: {} "
                                              "\nТочный адрес: {} "
                                              "\nСсылка на навигатор: {} "
                                              "\nСсылка на панораму(работает только на ПК): {}".format(r.name,
                                                                                                       r.phone,
                                                                                                       r.address,
                                                                                                       r.map,
                                                                                                       r.panorama))
            log(message, r)


# Напоминалка
@bot.message_handler(commands=['remind'])
def remind(message):
    raw = message.text
    if len(raw) < 8:
        bot.send_message(message.chat.id, "Введите время и дату как в примере команды /help")
    else:
        info = raw[7:len(raw)]
        info = info.split(" ")
        date = info[1]
        tim = info[2]
        tim2 = info[3]
        bot.send_message(message.chat.id,
                         "Напоминание настроено на \nЧисло: {} \nВремя: {} \nВремя напоминания {}".format(date,
                                                                                                          tim,
                                                                                                          tim2))

        def reminder():
            bot.send_message(message.chat.id,
                             "Напоминание, ваше собеседование пройдет \nЧисло: {} \nВремя: {}".format(date, tim))

        schedule.every().day.at(tim2).do(reminder)
        while True:
            schedule.run_pending()
            time.sleep(1)


bot.polling(none_stop=True, interval=0)
