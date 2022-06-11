from django.contrib.auth.models import User, Group
from rest_framework import serializers, fields
from sites.models import Password


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Password
        fields = ['expiration_date','max_views','views','password']

class PasswordGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Password
        fields = ['password']