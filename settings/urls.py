from django.contrib import admin
from django.urls import path
from bot.views import web_hook
from django.views.decorators.csrf import csrf_exempt
from users.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hook/', csrf_exempt(web_hook)),
    path('', test_page),
]
