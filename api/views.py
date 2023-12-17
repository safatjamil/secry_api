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


@api_view(["POST", "PUT", "DELETE"])
def user_registration(request):
    x = request.headers
    print(x)
    if request.method == "POST":
        try:
            data  = request.data
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
 
                # check duplicate account
                if query.check_duplicate_user(data["email"])>0:
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Account with this email already exists",
                        "data": serializer.data,
                        })
                
                # encrypt password
                data["password"] = encrypt.hash_password(data["password"])
                if "last_name" not in data:
                    data["last_name"] = ""
                
                # create user
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


    if request.method == "PUT":
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