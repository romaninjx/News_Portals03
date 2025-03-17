from django.urls import path
# Импортируем созданное нами представление
from .views import *





urlpatterns = [
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('user_lk/', IndexView.as_view(), name='user_lk'),
    ]