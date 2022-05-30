from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.repositories import password_repository
from api.serializers import password_serializer
from generator.entities.password import Password
from generator.services import password_service

# Create your views here.


class PasswordList(APIView):
    def get(self, request):
        passwords = password_service.get_passwords()
        serializer = password_serializer.PasswordSerializer(passwords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordDetails(APIView):
    def get(self, request, size):
        repository_password = password_repository.PasswodRepository(size)
        password = Password(
            value=repository_password.generate_password(),
            expiration_date=None,
            maximum_views=None,
            views=None
        )
        serializer = password_serializer.PasswordSerializer(password)
        return Response(serializer.data, status=status.HTTP_200_OK)
