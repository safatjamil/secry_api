from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import UserManager, CustomUser, Secret, EncKey
from modules import auth, cryptography, query, \
                    validations, jwt, dbase_operations


# modules
auth = auth.Auth()
encrypt = cryptography.Encrypt()
decrypt = cryptography.Decrypt()
validate = validations.Validations()
query = query.Query()
create = dbase_operations.Create()
update = dbase_operations.Update()
delete = dbase_operations.Delete()
User = get_user_model()


@api_view(["POST"])
def user_registration(request):
    try:
        data = request.data
        # clean data
        data["email"] = data["email"].strip()
        data["first_name"] = data["first_name"].strip()
        data["last_name"] = data["last_name"].strip()
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            create.user(data=data)
            return Response({"status": status.HTTP_201_CREATED,
                             "message": "Account has been created",
                             "data": serializer.data})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Please provide valid data",
                             "data": serializer.errors})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


# This method is to authenticate user by the email and password
@api_view(["GET"])
def user_authentication(request):
    try:
        data = request.data
        if ("email" in data and 
            "password" in data):
            verification = auth.user(email=data["email"].strip(), 
                                     password=data["password"])
            if verification:
                return Response({"status": status.HTTP_200_OK,
                                 "message": "Ok",
                                 "data": {}})
            else:
                return Response({"status": status.HTTP_401_UNAUTHORIZED,
                                 "message": "Unauthorized",
                                 "data" : {}})

        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Please provide valid data",
                             "data" : {}})

    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def user_view_account(request):
    try:
        user = request.user
        data = {"email": user.email, 
                "first_name": user.first_name, 
                "last_name": user.last_name}
        return Response({"status": status.HTTP_200_OK,
                         "message": "Account details",
                         "data": data})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_edit_email(request):
    try:
        data  = request.data
        user = request.user
        # requires password to change email
        if "password" in data:
            # verify the user
            verification = auth.user(email=user.email, 
                                     password=data["password"])
        
            if verification:
                if ("new_email" in data and 
                    validate.email(data["new_email"])):
                    if query.duplicate_user(data["new_email"]) > 0:
                        return Response({"status": status.HTTP_406_NOT_ACCEPTABLE,
                                         "message": "Account with this email already exists",
                                         "data": {}})
                    # update user
                    user.email = data["new_email"]
                    user.save()
                    return Response({"status": status.HTTP_201_CREATED,
                                     "message": "Your email address has been updated",
                                     "data": {}})
                else:
                    return Response({"status": status.HTTP_400_BAD_REQUEST,
                                     "message": "Please provide valid data",
                                     "data": {}})
            else:
                return Response({"status": status.HTTP_401_UNAUTHORIZED,
                                 "message": "Unauthorized",
                                 "data" : {}})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Please provide valid data",
                             "data" : {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})   


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_edit_info(request):
    try:
        data  = request.data
        user = request.user
        # assign a dummmy value to the last_name field if not sent
        if "last_name" not in data:
            data["last_name"] = ""
        if ("first_name" not in data or 
            data["first_name"].strip() == ""):
            return Response({"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Please provide valid data",
                             "data": {}})
        else:
            # update user data
            user_data = {"first_name": data["first_name"].strip(), 
                         "last_name": data["last_name"].strip()}
            update.user(user=user, data=user_data)
            return Response({"status": status.HTTP_201_CREATED,
                             "message": "Your account has been updated",
                             "data" : {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def user_change_password(request):
    try:
        data  = request.data
        user = request.user
        if "old_password" in data:
            verification = auth.user(email=user.email, 
                                     password=data["old_password"])
            if verification:
                user.set_password(data["new_password"])
                user.save()
                return Response({"status": status.HTTP_201_CREATED,
                                 "message": "Your password has been changed",
                                 "data": {}})
            else:
                return Response({"status": status.HTTP_401_UNAUTHORIZED,
                                 "message": "Unauthorized",
                                 "data" : {}})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Please provide valid data",
                             "data" : {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated,])
def delete_user(request):
    try:
        data = request.data
        user = request.user
        # verify the password
        if "password" in data:
            # verify the user
            verification = auth.user(email=user.email, 
                                     password=data["password"])
            if verification:
                secrets = query.secrets(user_id=user.id)
                # delete all the secrets first
                for secret in secrets:
                    delete.secret(secret_id=secret.id)
                    delete.enckey(secret_id=secret.id)
                # delete the user
                delete.user(user=user)
                return Response({"status": status.HTTP_200_OK,
                                 "message": "Your account has been destroyed. Sorry to see you go",
                                 "data": {}})
            else:
                return Response({"status": status.HTTP_401_UNAUTHORIZED,
                                 "message": "Unauthorized",
                                 "data" : {}})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Please provide valid data",
                             "data" : {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})
