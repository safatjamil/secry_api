from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import User
from modules.auth import *
from modules.encrypt import *
from modules.query import *
from modules.dbase_operations import *

auth = Auth()
encrypt = Encrypt()
query = Query()
create = Create()
update = Update()


@api_view(["POST"])
def user_registration(request):
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
                "message": "Unsuccessful operation",
                "data": serializer.errors
            })

    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Please provide valid data",
            "data" : {}
        })



@api_view(["PUT"])
@permission_classes([AllowAny, ])
def user_modification(request):
    try:
        data  = request.data
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            # check duplicate account
            if query.check_duplicate_user(data["new_email"])>0:
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Account with this email already exists",
                    "data": serializer.data,
                    })
        
            # update user
                create.user(data)
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
            "message": "Something went wrong",
            "data" : {}
            })