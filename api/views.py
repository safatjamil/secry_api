from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from modules.auth import *
from modules.encrypt import *
from modules.query import *
from modules.validations import *
from modules.jwt import *
from modules.dbase_operations import *

auth = Auth()
encrypt = Encrypt()
validate = Validations()
query = Query()
create = Create()
update = Update()

User = get_user_model()

@api_view(["POST"])
def user_registration(request):
    try:
        data = request.data
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = User.objects.create_user(email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"])
            return Response({
                "status": 200,
                "message": "Account has been created",
                "data": serializer.data,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Please provide valid data",
                "data": serializer.errors
            })

    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Something went wrong",
            "data" : {}
        })


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_edit_email(request):
    try:
        data  = request.data
        email = request.user.email
        print(email)
        print("1")
        print(validate.email(data["new_email"]))
        if "new_email" in data and validate.email(data["new_email"]):
            print("2")
            if query.duplicate_user(data["new_email"])>0:
                return Response({
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                    "message": "Account with this email already exists",
                    "data": {},
                    })
            # update user
            user = User.objects.get(email = data["old_email"])
            user.email = data["new_email"]
            user.save()
            return Response({
                "status": 200,
                "message": "Your email has been updated",
                "data": {},
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Please provide valid data",
                "data": {}
            })

    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Something went wrong",
            "data" : {}
            })

@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_edit_info(request):
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