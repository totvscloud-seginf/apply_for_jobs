from django.urls import path
from api.views import *

urlpatterns = [
    #post
    path('password', PasswordApiView.as_view(), name='passwords'),
    #get, put, delete
    path('password/<str:id>', PasswordApiView.as_view(), name='passwords'),
    #get
    path('password/size/<int:size>', PasswordGeneratorApiView.as_view(), name='passwords-gen'),
]

