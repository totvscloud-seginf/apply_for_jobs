from rest_framework import serializers

from generator.models import Password


class PasswordSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=50)
