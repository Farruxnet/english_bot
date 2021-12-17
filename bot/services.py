from data.models import Words
import telebot
from telebot import types
import random
from django.conf import settings
bot = telebot.TeleBot(settings.TOKEN)
from users.models import *
import datetime
count = 4

class MakeDictionary:
    def __init__(self, count, object):
        # self.dic = dic
        self.count = count
        self.object = object

    def make_json(self):
        """ Bazadan kelgan datani jsonga convert qiladi """
        json_result = {}

        for j in self.object:
            for idx in j.words.all():
                json_result[idx.id] = {"oz": idx.oz, "en": idx.en}

        return json_result

    def make_random_quiz(self):
        """ json ko'rinishida kelgan datani 4 ta
        random savolini[0] ja to'g'ri javobini qaytaradi[1] """
        try:
            word = self.make_json()
            random_word = random.sample(list(word), self.count)
            select = random_word[0]
            new_dictionary = list()
            new_dictionary.append(word[select])
            for i in random_word:
                if i != select:
                    new_dictionary.append(word[i])
                    return new_dictionary, word[select]
        except Exception as e:
            print(e)

    def make_button(self):
        """ tayyor kelgan json ko'rinishidagi datani
        telegram inline button objectini qaytaradi """
        quiz = self.make_random_quiz()
        button_text = set()
        for i in quiz[0]:
            if i['en'] == quiz[1]['en']:
                button_text.add(types.InlineKeyboardButton(text=i['en'], callback_data='True'))
            else:
                button_text.add(types.InlineKeyboardButton(text=i['en'], callback_data='False'))
        payment_method_button = types.InlineKeyboardMarkup(row_width=2)
        payment_method_button.add(*button_text)

        return payment_method_button, quiz[1]['oz']

def make_button(user_id):
    user_id = user_id
    print(user_id)
    def make_dic():
        """ Bazadan kelgan datani jsonga convert qiladi """
        result = {}
        for j in DayWord.objects.filter(user__tg_id = user_id, create_at__day = datetime.datetime.now().day):
            print(j.words.all())
            for idx in j.words.all():
                print(idx)
                result[idx.id] = {"oz": idx.oz, "en": idx.en}
        print(result)
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
