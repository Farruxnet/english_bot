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
    home_button.add(*[LAN['info'], LAN['start_new_lesson']])
    home_button.add(*[LAN['settings']])

    return home_button

def home_get(message, bot):
    bot.send_message(message.chat.id, LAN['start_text'], reply_markup = home_button(), parse_mode = 'html')
    User.objects.filter(tg_id = message.chat.id).update(step = STEP['DEFAULT'])

def start_lesson_button():
    start_lesson_button = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    start_lesson_button.add(*[LAN['basic_test'], LAN['new_word']])
    start_lesson_button.add(*[LAN['home']])

    return start_lesson_button
