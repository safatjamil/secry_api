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
from modules.jwt import *
from modules.dbase_operations import *

auth = Auth()
encrypt = Encrypt()
query = Query()
create = Create()
update = Update()


@api_view(["POST"])
def user_registration(request):
    try:
        data = request.data
        print("1")
        serializer = UserSerializer(data = request.data)
        print("2")
        if serializer.is_valid():

            print("3")
            print(serializer.data)
            user = CustomUser.objects.create_user(email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"])
        
            print("5")
            return Response({
                "status": 200,
                "message": "Account has been created",
                "data": serializer.data,
            })
        else:
            print("4")
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


@api_view(["POST"])
def user_login(request):
    try:
        data = request.data
        serializer = UserAuthSerializer(data = request.data)
        if serializer.is_valid():
            user = auth.user(email = data["email"], password = data["password"])
            if user is not None:
                tokens = create_tokens_for_user(user)
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "authorized",
                    "data": { "tokens" : tokens }
                   })

            else:
                return Response({
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Unauthorized",
                    "data": serializer.errors
                   })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Please provide valid data",
                "data" : {}
               })

    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Something went wrong",
            "data" : {}
        })

@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_edit(request):
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

@api_view(["POST"])
def authenticate_user(request):
    try:
        user = User.objects.get(email = request.data["email"], password = request.data["email"])
        if user:
            try:
                payload = jwt_payload_handler(user)

                token = jwt.encode(payload, settings.SECRET_KEY)

                user_details = {}

                user_details['name'] = "%s %s" % (

                    user.first_name, user.last_name)

                user_details['token'] = token

                user_logged_in.send(sender=user.__class__,

                                    request=request, user=user)

                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:

                raise e

        else:

            res = {

                'error': 'can not authenticate with the given credentials or the account has been deactivated'}

            return Response(res, status=status.HTTP_403_FORBIDDEN)

    except KeyError:

        res = {'error': 'please provide a email and a password'}

        return Response(res)
