from functools import partial
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from sites.models import Password
from .serializers import PasswordSerializer, PasswordGeneratorSerializer
from api.repositories import password_repository

from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime,timedelta, date

# Create your views here.
class PasswordApiView(APIView):
    def get(self,rq,id):
        '''
        Lista senha com base no id passado
        '''
        try:
            passwords_instance = Password.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"res": "Password with id does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordSerializer(passwords_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, rq, *args, **kwargs):
        '''
        Cria uma senha com os dados enviados
        '''

        #converte a quantidade de dias em um valor date valido
        pDias = int(rq.data.get('expiration_date'))
        data_calculada = password_repository.Password.calculate_expiration_date(pDias)

        #cria objeto/json do valor a ser inserido
        data = {
            'password': rq.data.get('password'), 
            'expiration_date': data_calculada.date(), 
            'max_views': rq.data.get('max_views'),
            'views': 0
        }
        serializer = PasswordSerializer(data=data)
        if serializer.is_valid():
            ser = serializer.save()
            return Response({"id": str(ser.id)}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, rq, id, *args, **kwargs):
        '''
        Atualiza uma senha com os valores enviados com base no id passado
        '''
        try:
            passwords_instance = Password.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"res": "Password with id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        #pDias = int(rq.data.get('expiration_date'))
        #data_calculada = password_repository.Password.calculate_expiration_date(pDias)
        data = {
            'password': rq.data.get('password'), 
            'expiration_date':  rq.data.get('expiration_date'), #data_calculada.date(), 
            'max_views': rq.data.get('max_views'),
            'views': rq.data.get('views')
        }            
        
        serializer = PasswordSerializer(instance=passwords_instance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id, *args, **kwargs):
        '''
        Deleta senha com base no id passado
        '''
        try:
            passwords_instance = Password.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"res": "Password with id does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        passwords_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)




class PasswordGeneratorApiView(APIView):
        def get(self,rq,size):
            '''
            Gera uma senha com o limite de tamanho passado
            '''
            resp_password = password_repository.Password(size)
            password = {
                'password': resp_password.generate_password(), 
                'expiration_date': None, 
                'max_views': None,
                'views': None
            }
            serializer = PasswordGeneratorSerializer(password)
            if resp_password:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)