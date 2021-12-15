from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
import telebot
from django.conf import settings
bot = telebot.TeleBot(settings.TOKEN)
import os
import requests
import threading, time
import traceback
from django.db.models import Q
from. models import TextData, Words

@receiver(post_save, sender=TextData)
def file(sender, instance, created, **kwargs):
    if created:
        file_path = f'{settings.MEDIA_ROOT}/{TextData.objects.get(id = int(str(instance))).file}'
        obj = []
        try:
            with open(file_path, 'r') as f:
                for i in f:
                    en = i.split('-')[0].capitalize()
                    oz = i.split('-')[1].capitalize()
                    if not Words.objects.filter(oz = oz, en = en).exists():
                        obj.append(Words(oz = oz, en = en))
            if obj:
                Words.objects.bulk_create(obj)
        except Exception as e:
            print(e)
    else:
        print('update')
