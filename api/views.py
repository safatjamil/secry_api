from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class UserRegistrationView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "Account has been created",
                    "data": serializer.data,
                })

        except:
            return Response({
                    "status": 403,
                    "message": "Bad format",
                    "data": serializer.data,
                })