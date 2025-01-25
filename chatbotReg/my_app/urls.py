from django.urls import path
from .views import random_greeting, register_bhandara, get_all_bhandara_records

urlpatterns = [
    path('greet/', random_greeting, name='greet'),
    path('register/', register_bhandara, name='register_bhandara'),
    path('get_all_bhandara_records/', get_all_bhandara_records, name='get_all_bhandara_records'),

]
