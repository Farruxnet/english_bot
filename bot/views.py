from django.shortcuts import render, HttpResponse
import telebot
from telebot import types
from django.conf import settings
from data.models import Words

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


@bot.message_handler(func=lambda msg: True)
def home_go(message):
    print(list(Words.objects.all()))
    try:
        payment_method_button = types.InlineKeyboardMarkup(row_width=2)
        payment_method_button.add(
            types.InlineKeyboardButton(text='Hello', callback_data='click'),
            types.InlineKeyboardButton(text='Programmer', callback_data='payme'),
            types.InlineKeyboardButton(text='Cry', callback_data='paynet'),
            types.InlineKeyboardButton(text='Cat', callback_data='paynet'),
        )
        bot.send_message(message.from_user.id, 'text', reply_markup = payment_method_button)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: True)
def get_call_back(call):
    print(call.data)
