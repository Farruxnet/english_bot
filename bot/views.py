from django.shortcuts import render, HttpResponse
import telebot
from telebot import types
from django.conf import settings
from data.models import Words
import random
from . services import MakeDictionary
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
            new_user(message, bot)
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

@bot.message_handler(func=lambda msg: msg.text == LAN['new_word'])
def bot_new_words(message):
        if DayWord.objects.filter(user__tg_id = message.chat.id, create_at__day = datetime.datetime.now().day).exists():
            start_test_button = types.InlineKeyboardMarkup(row_width=2)
            start_test_button.add(
                types.InlineKeyboardButton(
                    text=LAN['start_test'],
                    callback_data='start'
                )
            )
            exists_word = DayWord.objects.get(user__tg_id = message.chat.id, create_at__day = datetime.datetime.now().day)
            bot.send_message(
                message.chat.id,
                text = exists_word.words_text + exists_word.create_at.strftime("\n<b><i>%Y-%m-%d sana uchun</i></b>"),
                reply_markup = start_test_button,
                parse_mode = 'html'
            )
        else:
            try:
                message_id = bot.send_message(message.chat.id, LAN['wait']).message_id
                DayWord.objects.create(
                    user = User.objects.get(tg_id = message.chat.id),
                )
                Ball.objects.create(
                    user = User.objects.get(tg_id = message.chat.id),
                )
                UserNewWord.objects.create(
                    user = User.objects.get(tg_id = message.chat.id),
                )
                day_word = DayWord.objects.filter(user__tg_id = message.chat.id, create_at__day = datetime.datetime.now().day)
                for c, i in zip(range(1, 26), Words.objects.all()):
                    for j in day_word:
                        if not j.words.filter(oz__in = [i.oz], en__in = [i.en]).exists():
                            DayWord.objects.update_or_create(
                                user__tg_id=message.chat.id,
                                create_at__day = datetime.datetime.now().day
                            )[0].words.add(
                                Words.objects.get(id = i.id)
                            )
                            if c == 25:
                                break
                word = ''
                for i in DayWord.objects.filter(user__tg_id = message.chat.id, create_at__day = datetime.datetime.now().day):
                    for d, k in zip(range(1, 31), i.words.all()):
                        word += f'{d}. {k.en} - {k.oz}'
                day_word.update(words_text = word)
                bot.delete_message(message_id = message_id, chat_id = message.chat.id)
                start_test_button = types.InlineKeyboardMarkup(row_width=2)
                start_test_button.add(
                    types.InlineKeyboardButton(
                        text=LAN['start_test'],
                        callback_data='start'
                    )
                )
                bot.send_message(
                    message.chat.id,
                    text = word,
                    reply_markup = start_test_button,
                    parse_mode = 'html'
                )

            except Exception as e:
                print(e)

@bot.message_handler(func=lambda msg: msg.text == LAN['settings'])
def bot_settings(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def get_call_back(call):
    data = call.data
    dictionary_obj = DayWord.objects.filter(user__tg_id = call.message.chat.id, create_at__day = datetime.datetime.now().day)
    obj = MakeDictionary(4, dictionary_obj)
    mb = obj.make_button()
    if data == 'start':
        try:
            bot.edit_message_text(
                message_id = call.message.message_id,
                chat_id = call.message.chat.id,
                text = mb[1],
                reply_markup = mb[0]
            )
        except Exception as e:
            print(e)

    elif data == 'True' or data == 'False':
        if data == 'True':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="To'g'ri ✅")
        elif data == 'False':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Noto'g'ri ❌")
        try:
            try:
                bot.edit_message_text(
                    message_id = call.message.message_id,
                    chat_id = call.message.chat.id,
                    text = mb[1],
                    reply_markup = mb[0]
                )
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)




































    #
