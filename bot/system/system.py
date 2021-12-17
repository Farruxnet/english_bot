import telebot
from telebot import types
import random
from django.conf import settings
from . language import LAN
from . step import STEP
bot = telebot.TeleBot(settings.TOKEN)
from users.models import *


def home_button():
    home_button = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    home_button.add(*[LAN['start_new_lesson'], LAN['info']])
    home_button.add(*[LAN['settings']])

    return home_button

def home_get(message, bot):
    bot.send_message(message.chat.id, LAN['start_text'], reply_markup = home_button(), parse_mode = 'html')
    User.objects.filter(tg_id = message.chat.id).update(step = STEP['DEFAULT'])

def new_user(message, bot):
    if message.chat.last_name:
        name = message.chat.first_name + ' ' + message.chat.last_name
    else:
        name = message.chat.first_name
    User.objects.create(
        tg_id = message.chat.id,
        name = name,
        username = message.chat.username
    )
    home_get(message, bot)



def start_lesson_button():
    start_lesson_button = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    start_lesson_button.add(*[LAN['new_word'], LAN['basic_test']])
    start_lesson_button.add(*[LAN['saved_word']])
    start_lesson_button.add(*[LAN['home']])

    return start_lesson_button
