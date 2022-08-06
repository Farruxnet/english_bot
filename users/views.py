from django.shortcuts import render
from django.conf import settings
from data.models import *
import random
from bot.services import MakeDictionarySite

def test_page(request):
    r1 = Words.objects.all()[:10]
    r2 = Words.objects.all()[:10]
    r3 = Words.objects.all()[:10]
    r4 = Words.objects.all()[:10]
    dictionary_obj = Words.objects.all()
    obj = MakeDictionarySite(10, dictionary_obj)
    print(obj.make_json())
    data = {
        "answer": obj.make_json()
    }
    return render(request, 'index.html', data)
