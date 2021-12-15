from django.shortcuts import render, HttpResponse
import telebot
from telebot import types
from django.conf import settings
from data.models import Words
import random
from . services import make_button

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
        start_button = types.InlineKeyboardMarkup(row_width=2)
        start_button.add(types.InlineKeyboardButton(text="Boshlash", callback_data='start'))
        bot.send_message(message.from_user.id, "Boshlash!", reply_markup = start_button)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: True)
def get_call_back(call):
    import traceback
    data = call.data
    if data == 'start':
        bot.delete_message(message_id = call.message.message_id, chat_id = call.message.chat.id)
        try:
            button = make_button()
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
            button = make_button()
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
