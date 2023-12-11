from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "Account has been created",
                    "data": serializer.data,
                })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Bad format",
                    "data": serializer.errors
                })

        except:
            return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Can not parse data",
                    "data" : {}
                })