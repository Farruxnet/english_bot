from data.models import Words
import telebot
from telebot import types
import random
from django.conf import settings
bot = telebot.TeleBot(settings.TOKEN)


count = 4

def make_dic():
    """ Bazadan kelgan datani jsonga convert qiladi """
    result = {}
    for idx in Words.objects.all():
        result[idx.id] = {"oz": idx.oz, "en": idx.en}
    return result

def random_question_answer(word):
    """ json ko'rinishida kelgan datani 4 ta
    random savolini[0] ja to'g'ri javobini qaytaradi[1] """

    random_word = random.sample(list(word), count)
    select = random_word[0]
    new_dictionary = list()
    new_dictionary.append(word[select])
    for i in random_word:
        if i != select:
            new_dictionary.append(word[i])
    return new_dictionary, word[select]


def make_button():
    """ tayyor kelgan json ko'rinishidagi datani
    telegram inline button objectini qaytaradi """
    quiz = random_question_answer(make_dic())
    button_text = set()
    for i in quiz[0]:
        if i['en'] == quiz[1]['en']:
            button_text.add(types.InlineKeyboardButton(text=i['en'], callback_data='True'))
        else:
            button_text.add(types.InlineKeyboardButton(text=i['en'], callback_data='False'))
    payment_method_button = types.InlineKeyboardMarkup(row_width=2)
    payment_method_button.add(*button_text)

    return payment_method_button, quiz[1]['oz']
