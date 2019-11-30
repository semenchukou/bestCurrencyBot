import telebot
from telebot import types
import pageParsing
from PIL import Image
import datetime

bot = telebot.TeleBot('') ######################

date = datetime.datetime.now().strftime("%d-%m-%Y")
currency = ''
to_buy = False

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, text="Choose currency", reply_markup = get_choose_currency_keyboard())
    elif message.text == "/history":
        bot.send_message(message.from_user.id, text="Choose currency", reply_markup = get_history_keyboard())
    else:
        bot.send_message(message.from_user.id, "/start - start currency getting procedure \n/history - get best currency graph for the last month")

def get_history_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_eur = types.InlineKeyboardButton(text = 'EUR', callback_data = 'EUR_HIST')
    key_usd= types.InlineKeyboardButton(text = 'USD', callback_data = 'USD_HIST')
    key_rub= types.InlineKeyboardButton(text = 'RUB', callback_data = 'RUB_HIST')
    keyboard.add(key_eur, key_usd, key_rub)
    return keyboard

def get_choose_currency_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_eur = types.InlineKeyboardButton(text = 'EUR', callback_data = 'EUR')
    key_usd= types.InlineKeyboardButton(text = 'USD', callback_data = 'USD')
    key_rub= types.InlineKeyboardButton(text = 'RUB', callback_data = 'RUB')
    keyboard.add(key_eur, key_usd, key_rub)
    return keyboard

def get_choose_option_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_buy = types.InlineKeyboardButton(text = 'BUY', callback_data = 'BUY')
    key_sell = types.InlineKeyboardButton(text = 'SELL', callback_data = 'SELL')
    key_history = types.InlineKeyboardButton(text = 'BACK', callback_data = 'back')
    keyboard.add(key_buy, key_sell, key_history)
    return keyboard

def send_result_to_user(url, chat_id, to_buy, currency):
    name, value, address = pageParsing.parse_for_best_values(url, to_buy)
    if to_buy == True:
        bot.send_message(chat_id, 'Bank with the best rate to buy ' + currency + ': ' + name + '\n' + 'rate : ' + str(value) + '\n' + 'address : ' + address)
    else:
        bot.send_message(chat_id, 'Bank with the best rate to sell ' + currency + ': ' + name + '\n' + 'rate : ' + str(value) + '\n' + 'address : ' + address)
    address_lat_long = pageParsing.extract_lat_long_via_address(address)
    bot.send_location(chat_id, float(address_lat_long[1]), float(address_lat_long[0]))

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global currency
    if call.data == 'back':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Choose option", reply_markup = get_choose_currency_keyboard())
    elif call.data == "EUR":
        currency = "EUR"
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Choose option", reply_markup = get_choose_option_keyboard())
    elif call.data == "USD":
        currency = "USD"
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Choose option", reply_markup = get_choose_option_keyboard())
    elif call.data == "RUB":
        currency = "RUB"
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Choose option", reply_markup = get_choose_option_keyboard())
    elif call.data == 'BUY':
        if currency == 'USD':
            send_result_to_user('https://finance.tut.by/kurs/minsk/dollar/?sortBy=sell&sortDir=up', call.message.chat.id, False, 'USD')
        elif currency == 'EUR':
            send_result_to_user('https://finance.tut.by/kurs/minsk/euro/?sortBy=sell&sortDir=up', call.message.chat.id, False, 'EUR')
        elif currency == 'RUB':
            send_result_to_user('https://finance.tut.by/kurs/minsk/rubl/?sortBy=sell&sortDir=up', call.message.chat.id, False, 'RUB')
    elif call.data == 'SELL':
        if currency == 'USD':
            send_result_to_user('https://finance.tut.by/kurs/minsk/dollar/?sortBy=buy&sortDir=down', call.message.chat.id, True, 'USD')
        elif currency == 'EUR':
            send_result_to_user('https://finance.tut.by/kurs/minsk/euro/?sortBy=buy&sortDir=down', call.message.chat.id, True, 'EUR')
        elif currency == 'RUB':
            send_result_to_user('https://finance.tut.by/kurs/minsk/rubl/?sortBy=buy&sortDir=down', call.message.chat.id, True, 'RUB')
    elif call.data == 'USD_HIST':
        buf = pageParsing.parse_for_history_and_build_figure('https://finance.tut.by/arhiv/?currency=USD&date=' + date, 'USD')
        bot.send_photo(call.message.chat.id, photo = buf)
        buf.close()
    elif call.data == 'EUR_HIST':
        buf = pageParsing.parse_for_history_and_build_figure('https://finance.tut.by/arhiv/?currency=EUR&date=' + date, 'EUR')
        bot.send_photo(call.message.chat.id, photo = buf)
        buf.close()
    elif call.data == 'RUB_HIST':
        buf = pageParsing.parse_for_history_and_build_figure('https://finance.tut.by/arhiv/?currency=RUB&date=' + date, 'RUB')
        bot.send_photo(call.message.chat.id, photo = buf)
        buf.close()

bot.polling(none_stop=True)