from django.shortcuts import render, HttpResponse
import telebot
from telebot import types
from django.conf import settings
from data.models import Words
import random
from . services import make_button
from users.models import *
import datetime
from . language import LAN
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
    if User.objects.filter(tg_id = message.chat.id).exists():
        start_button = types.InlineKeyboardMarkup(row_width=2)
        start_button.add(
            types.InlineKeyboardButton(
                text=LAN['start_lesson'],
                callback_data='begin'
            )
        )
        bot.send_message(message.from_user.id, "", reply_markup = start_button, parse_mode = 'html')

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
        start_button = types.InlineKeyboardMarkup(row_width=2)
        start_button.add(
            types.InlineKeyboardButton(
                text="So'z yodlashni boshlash",
                callback_data='begin'
            )
        )
        bot.send_message(message.from_user.id, LAN["start_text"], reply_markup = start_button, parse_mode = 'html')



@bot.callback_query_handler(func=lambda call: True)
def get_call_back(call):
    import traceback
    data = call.data
    obj = DayWord.objects.filter(user__tg_id = call.message.chat.id, create_at__day = datetime.datetime.now().day)
    if data == 'begin':
        if obj.exists():
            word = ''
            for i in obj:
                for d, k in zip(range(1, 31), i.words.all()):
                    word += f'{d}. {k.en} - {k.oz}'
            start_test_button = types.InlineKeyboardMarkup(row_width=2)
            start_test_button.add(
                types.InlineKeyboardButton(
                    text="Testni boshlash",
                    callback_data='start'
                )
            )
            bot.edit_message_text(
                message_id = call.message.message_id,
                chat_id = call.message.chat.id,
                text = word,
                reply_markup = start_test_button,
                parse_mode = 'html'
            )
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Bugun sizga 30 ta so'z berilgan!")
        else:
            bot.delete_message(message_id = call.message.message_id, chat_id = call.message.chat.id)
            try:
                DayWord.objects.create(
                    user = User.objects.get(tg_id = call.message.chat.id),
                )
                Ball.objects.create(
                    user = User.objects.get(tg_id = call.message.chat.id),
                )
                UserNewWord.objects.create(
                    user = User.objects.get(tg_id = call.message.chat.id),
                )
            except Exception as e:
                print(e)
            for c, i in zip(range(1, 31), Words.objects.all()):
                for j in DayWord.objects.filter(user__tg_id = call.message.chat.id):
                    if not j.words.filter(oz__in = [i.oz], en__in = [i.en]).exists():
                        print(c, i)
                        DayWord.objects.update_or_create(
                            user__tg_id=call.message.chat.id,
                        )[0].words.add(
                            Words.objects.get(id = i.id)
                        )
                        if c == 30:
                            break
            try:
                word = ''
                for i in DayWord.objects.filter(user__tg_id = call.message.chat.id, create_at__day = datetime.datetime.now().day):
                    for d, k in zip(range(1, 31), i.words.all()):
                        word += f'{d}. {k.en} - {k.oz}'
                        start_test_button = types.InlineKeyboardMarkup(row_width=2)
                        start_test_button.add(
                            types.InlineKeyboardButton(
                                text="Testni boshlash",
                                callback_data='start'
                            )
                        )
                bot.send_message(call.message.chat.id, 'Kutib turing')
                bot.delete_message(message_id = call.message.message_id, chat_id = call.message.chat.id)
                bot.send_message(
                    call.message.chat.id,
                    text = word,
                    reply_markup = start_test_button,
                    parse_mode = 'html'
                )
            except Exception as e:
                print(e)
    elif data == 'start':
        bot.delete_message(message_id = call.message.message_id, chat_id = call.message.chat.id)
        try:
            button = make_button(call.message.chat.id)
            bot.send_message(
                call.message.chat.id,
                text = '<b>Savol:</b> ' + str(button[1]) + '\n\n To`g`ri javobni belgilang 👇',
                reply_markup = button[0],
                parse_mode = 'html'
            )
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
    elif data == 'True' or data == 'False':
        if data == 'True':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="To'g'ri ✅")
        elif data == 'False':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Noto'g'ri ❌")
        try:
            button = make_button(call.message.chat.id)
            bot.edit_message_text(
                message_id = call.message.message_id,
                chat_id = call.message.chat.id,
                text = '<b>Savol:</b> ' + str(button[1]) + '\n\n To`g`ri javobni belgilang 👇',
                reply_markup = button[0],
                parse_mode = 'html'
            )
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
