from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from modules.auth import *
from modules.cryptography import *
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
        data["first_name"] = data["first_name"].strip()
        data["last_name"] = data["last_name"].strip()
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = User.objects.create_user(email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"])
            return Response({
                "status": status.HTTP_201_CREATED,
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
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong",
            "data" : {}
        })


# This authentication method is to authenticate user by the email and password
@api_view(["GET"])
def user_authentication(request):
    try:
        data = request.data
        if "email" in data and "password" in data:
            verification = auth.user(email=data["email"].strip(), password=data["password"])
        
            if verification:
                return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Ok",
                        "data": {},
                    })
            
            else:
                return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Unauthorized",
                "data" : {}
                })

        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Please provide valid data",
            "data" : {}
            })

    except:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong",
            "data" : {}
        })

@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def user_view_account(request):
    try:
        user = request.user
        print(user.id)
        print(user.email)
        data = {"email": user.email, "first_name": user.first_name, "last_name": user.last_name}
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Account details",
            "data": data,
           })

    except:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong",
            "data" : {}
           })


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_edit_email(request):
    try:
        data  = request.data
        user = request.user
        
        # requires password to change email
        if "email" in data and "password" in data:
            verification = auth.user(email=data["email"].strip(), password=data["password"])
        
            if verification:
                if "new_email" in data and validate.email(data["new_email"]):
                    if query.duplicate_user(data["new_email"])>0:
                        return Response({
                            "status": status.HTTP_406_NOT_ACCEPTABLE,
                            "message": "Account with this email already exists",
                            "data": {},
                            })
            
                    # update user
                    user.email = data["new_email"]
                    user.save()

                    return Response({
                        "status": status.HTTP_201_CREATED,
                        "message": "Your email address has been updated",
                        "data": {},
                    })
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Please provide valid data",
                        "data": {}
                    })
            else:
                return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Unauthorized",
                "data" : {}
                })
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Please provide valid data",
            "data" : {}
            })
        
    except:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong",
            "data" : {}
            })   


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_edit_info(request):
    try:
        data  = request.data
        user = request.user
        print(user.password)
        
        # assign a dummmy value to the last_name field if not sent
        if "last_name" not in data:
            data["last_name"] = ""
        
        if "first_name" not in data or data["first_name"].strip() == "":
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Please provide valid data",
                "data": {}
            })

        else:
            user.first_name = data["first_name"].strip()
            user.last_name = data["last_name"].strip()
            user.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Your account has been updated",
                "data" : {}
                })
    except:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong",
            "data" : {}
            })


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_change_password(request):
    try:
        data  = request.data
        user = request.user
        
        if "email" in data and "old_password" in data:
            verification = auth.user(email=data["email"].strip(), password=data["old_password"])
        
            if verification:
                user.set_password(data["new_password"])
                user.save()
                return Response({
                        "status": status.HTTP_201_CREATED,
                        "message": "Your password has been changed",
                        "data": {},
                    })
            
            else:
                return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Unauthorized",
                "data" : {}
                })

        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Please provide valid data",
            "data" : {}
            })
    except:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong",
            "data" : {}
            })


