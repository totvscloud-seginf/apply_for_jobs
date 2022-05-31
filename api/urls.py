from django.urls import path

from api.views import *

urlpatterns = [
    path('passwords/', PasswordList.as_view(), name='password-list'),
    path('passwords/value/size=<int:size>/', PasswordDetails.as_view(), name='password-details'),
]
