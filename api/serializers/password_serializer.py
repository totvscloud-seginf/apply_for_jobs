from rest_framework import serializers

from generator.models import Password


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value = self.data['value']

        if not value:
            raise serializers.ValidationError("400 Bad Request: O 'size' deve ser maior igual a 8 e menor igual 50.")
