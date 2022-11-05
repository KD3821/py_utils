import threading
from time import sleep

import telebot
from django.contrib.auth import authenticate

from accounts.models import UserConfirmCode
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import emoji
from telebot import types

API_TOKEN = "your_bot_token"

CODE_MESSAGE = "Код подтверждения: {0}"

bot = telebot.TeleBot(API_TOKEN, threaded=False)

bot.remove_webhook()
sleep(1)
#bot.set_webhook('https://touchip.ru/api/telegram/updates/' + API_TOKEN, max_connections=50)
bot.set_webhook('https://mysoft78.ru/api/telegram/updates/' + API_TOKEN, max_connections=50)

admin_chat_id = "admin_telegram_id"

emoji_pray = emoji.emojize(':pray:', language='alias')
emoji_rocket = emoji.emojize(':rocket:', language='alias')
emoji_checked = emoji.emojize(':white_check_mark:', language='alias')
emoji_key = emoji.emojize(':key:', language='alias')
emoji_lock = emoji.emojize(':lock:', language='alias')
emoji_unlock = emoji.emojize(':unlock:', language='alias')

button_get_code = types.InlineKeyboardButton('Получить код  ' + emoji_rocket, callback_data='wrng_nick')
button_get_code_again = types.InlineKeyboardButton("Теперь все верно. Хочу код  " + emoji_pray, callback_data='start_again')


keyboard_wrong = types.InlineKeyboardMarkup()
keyboard_wrong.add(button_get_code)
keyboard_start = types.InlineKeyboardMarkup()
keyboard_start.add(button_get_code_again)


# Process webhook calls
@csrf_exempt
def handle(request, token):
    if token == bot.token:
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def send_msg_to_admin_group(message):
    bot.send_message(admin_chat_id, message)


@bot.callback_query_handler(func=lambda m: True)
def callback_query(m):
    telegram_username = m.message.chat.username
    user_conf_code = UserConfirmCode.objects.filter(contact_type=UserConfirmCode.CONTACT_TYPE_TELEGRAM, contact_info=telegram_username).last()
    user_conf_code_exist = UserConfirmCode.objects.filter(contact_type=UserConfirmCode.CONTACT_TYPE_TELEGRAM, contact_info=str(m.message.chat.id)).last()
    if user_conf_code:
        user_conf_code.contact_info = m.message.chat.id
        user_conf_code.save()
        bot.send_message(m.message.chat.id, emoji_key + ' ' + CODE_MESSAGE.format(user_conf_code.code))
    elif user_conf_code_exist:
        bot.send_message(m.message.chat.id, emoji_checked + " Вы уже получили код подтверждения.")
    else:
        if m.data == 'wrng_nick':
            my_msg = emoji_lock + ' Вам необходимо указать верные данные на странице регистрации и затем нажать кнопку:'
            my_markup = keyboard_start
        elif m.data == 'start_again':
            my_msg = emoji_lock + ' Задан неверный никнейм. Пожалуйста, укажите верные данные на странице регистрации и нажмите :'
            my_markup = keyboard_wrong
        bot.send_message(m.message.chat.id, my_msg, reply_markup=my_markup)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    telegram_username = message.from_user.username
    user_conf_code = UserConfirmCode.objects.filter(contact_type=UserConfirmCode.CONTACT_TYPE_TELEGRAM,
                                                    contact_info=telegram_username).last()
    user_conf_code_exist = UserConfirmCode.objects.filter(contact_type=UserConfirmCode.CONTACT_TYPE_TELEGRAM,
                                                          contact_info=str(message.chat.id)).last()
    if user_conf_code:
        user_conf_code.contact_info = str(message.chat.id)
        user_conf_code.save()
        bot.send_message(message.chat.id, emoji_key + ' ' + CODE_MESSAGE.format(user_conf_code.code))
    elif user_conf_code_exist:
        bot.send_message(message.chat.id, emoji_checked + " Вы уже получили код подтверждения.")
    else:
        my_msg = emoji_lock + ' Код не найден. Возможно, вы ввели не верный никнейм. Введите корректный никнейм на странице регистрации, и затем нажмите кнопку:'
        bot.send_message(message.chat.id, my_msg, reply_markup=keyboard_wrong)


def send_msg(user_id, msg):
    bot.send_message(user_id, emoji_unlock + ' ' + msg)

