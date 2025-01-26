from django.urls import path
from .views import random_greeting, register_bhandara, get_all_bhandara_records, get_bhandara_by_abhyasi_id, \
    register_gitopadesh, get_gitopadesh_by_id, get_registrations, register_hope, get_hope_by_id, get_all_hope

urlpatterns = [
    path('greet/', random_greeting, name='greet'),
    path('register/', register_bhandara, name='register_bhandara'),
    path('get_all_bhandara_records/', get_all_bhandara_records, name='get_all_bhandara_records'),
    path('get_bhandara_by_abhyasi_id/<str:abhyasi_id>/', get_bhandara_by_abhyasi_id, name='get_bhandara_by_abhyasi_id'),
    path('gitopadesh/register/', register_gitopadesh, name='register_gitopadesh'),
    path('gitopadesh/get_by_id/<str:abhyasi_id>/', get_gitopadesh_by_id, name='get_gitopadesh_by_id'),
    path('gitopadesh/registrations/', get_registrations, name='get_registrations'),
    path('hope/register/', register_hope, name='register_hope'),
    path('hope/get_by_id/<str:abhyasi_id>/', get_hope_by_id, name='get_hope_by_id'),
    path('hope/get_all/', get_all_hope, name='get_all_hope'),

]

