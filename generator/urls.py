from django.urls import path

from generator.views import *

urlpatterns = [
    path('create/', create_password, name='create_password'),
    path('', get_passwords, name='get_passwords'),
    path('expirated/', delete_expirated, name='delete_expirated'),
    path('<str:id>/', get_password_id, name='get_password_id'),
    path('delete/<str:id>/', delete_password, name='delete_password'),
]
