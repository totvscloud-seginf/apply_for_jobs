from venv import create
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('password/<str:id>', views.get_password_id, name='get_password_id'),
    path('create', views.create_password, name='create_password')
]


