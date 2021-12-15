from django.shortcuts import render, HttpResponse
import telebot
from telebot import types
from django.conf import settings
from data.models import Words
import random
from . services import make_button
from users.models import *
import datetime
from bot.system import *

bot = telebot.TeleBot(settings.TOKEN)

def web_hook(request):
    if request.method == "POST":
        try:
            bot.process_new_updates([telebot.types.Update.de_json(request.body.decode('utf-8'))])
        except Exception as e:
            bot.send_message(313578337, f'web_hook error\n\n{e}')
            print(e)
            traceback.print_exc()
        return HttpResponse(status=200)
    s = '<a href="https://api.telegram.org/bot{0}/setWebhook?url={1}/hook/">WEB</a>'.format(settings.TOKEN, settings.WEBHOOK)
    return HttpResponse(s)


@bot.message_handler(commands = ['start'])
def start(message):
    try:
        if User.objects.filter(tg_id = message.chat.id).exists():
            home_get(message, bot)
        else:
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
    except Exception as e:
        print(e)


@bot.message_handler(func=lambda msg: msg.text == LAN['home'])
def info(message):
    home_get(message, bot)


@bot.message_handler(func=lambda msg: msg.text == LAN['info'])
def info(message):
    pass

@bot.message_handler(func=lambda msg: msg.text == LAN['start_new_lesson'])
def new_word(message):
    try:
        bot.send_message(message.chat.id, LAN['new_word'], parse_mode = 'html', reply_markup = start_lesson_button())
    except Exception as e:
        print(e)

@bot.message_handler(func=lambda msg: msg.text == LAN['settings'])
def settings(message):
    pass










































    #
