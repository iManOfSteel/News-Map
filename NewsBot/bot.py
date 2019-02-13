import telebot
import handler
from telebot import types
from collections import defaultdict

bot = telebot.TeleBot('774539506:AAHO_6iEdcV0UOZGGoIbZ24vyvNY6c2iMRo')

DEFAULT_STATE = 'default'
chat_states = defaultdict(lambda: DEFAULT_STATE)

START_MESSAGE = 'Привет, чего хочешь?'

ARTICLE_SENT_MESSAGE = 'Новость отправлена на обработку'
ARTICLE_PROCESSED_MESSAGE = 'Статья прошла проверку и скоро будет добавлена в базу'
ARTICLE_FAILED_MESSAGE = 'Кажется со статьей что-то не так'

MAP_FAILED_MESSAGE = 'Карта сейчас недоступна('

REG_PROCESSING_MESSAGE = 'Обрабатываем данные...'
REG_FAILED_MESSAGE = 'Кажется, что даже нам неизвестно как там дела -_-'

BTN_ARTICLE = 'Предложить новость'
BTN_MAP = 'Посмотреть карту'
BTN_REG = 'Как дела в ...'

BTNS = [BTN_ARTICLE, BTN_MAP, BTN_REG]

BTN_REPLIES = {
    BTN_ARTICLE: 'Кидай новость',
    BTN_MAP: 'Сейчас скину',
    BTN_REG: 'Кидай местоположение'
}

def on_map(message):
    cid = message.chat.id
    try:
        map_url = handler.process_map(message)
        bot.send_message(cid, map_url)
    except Exception as e:
        bot.send_message(cid, MAP_FAILED_MESSAGE)
    chat_states[cid] = DEFAULT_STATE


@bot.message_handler(commands=['start'])
def greetings(message):
    cid = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)
    btns = []
    btns.append(types.KeyboardButton(BTN_ARTICLE))
    btns.append(types.KeyboardButton(BTN_MAP))
    btns.append(types.KeyboardButton(BTN_REG))
    markup.row(*btns)
    bot.send_message(cid, START_MESSAGE, reply_markup=markup)


@bot.message_handler(func=lambda x: x.text in BTNS)
def on_btn_click(message):
    cid = message.chat.id
    chat_states[cid] = message.text
    bot.send_message(cid, BTN_REPLIES[message.text])
    if message.text == BTN_MAP:
        on_map(message)


@bot.message_handler(func=lambda m: chat_states[m.chat.id] == BTN_ARTICLE)
def on_article(message):
    cid = message.chat.id
    bot.send_message(cid, ARTICLE_SENT_MESSAGE)
    try:
        sc = handler.process_article(message.text)
        bot.send_message(cid, ARTICLE_PROCESSED_MESSAGE)
        bot.send_message(cid, 'Оценка новости: {}'.format(sc))
    except Exception as e:
        bot.send_message(cid, ARTICLE_FAILED_MESSAGE)
    chat_states[cid] = DEFAULT_STATE
        

@bot.message_handler(func=lambda m: chat_states[m.chat.id] == BTN_REG, content_types='location')
def on_reg(message):
    print(message.location)
    cid = message.chat.id
    bot.send_message(cid, REG_PROCESSING_MESSAGE)
    try:
        area, (summ, cnt) = handler.process_reg(
            longitude=message.location.longitude,
            latitude=message.location.latitude
        )
        bot.send_message(cid, "Местоположение: {}, оценка: {:.2f}".format(area, summ / cnt))
    except Exception as e:
        print(str(e))
        bot.send_message(cid, REG_FAILED_MESSAGE)
    chat_states[cid] = DEFAULT_STATE


@bot.message_handler(func=lambda m: chat_states[m.chat.id] == BTN_REG, content_types='text')
def on_reg(message):
    cid = message.chat.id
    try:
        summ, cnt = handler.process_reg_text(message.text)
        bot.send_message(cid, "Oценка: {:.2f}".format(summ / cnt))
    except Exception as e:
        print(str(e))
        bot.send_message(cid, REG_FAILED_MESSAGE)
    chat_states[cid] = DEFAULT_STATE


bot.polling()
