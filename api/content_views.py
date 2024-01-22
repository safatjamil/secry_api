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


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def user_view_secrets(request):
    try:
        user = request.user
        data = []
        secrets = query.secrets(user_id = user.id)
        # don't send the secret contents. The secret will be available in the detailed view(api/secret/<secret_id>)
        for secret in secrets:
            dict_ = {}
            dict_["id"] = secret.id
            dict_["title"] = secret.title
            data.append(dict_)
        return Response({"status": status.HTTP_200_OK,
                         "message": "Secrets",
                         "data": data})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


@api_view(["POST"])
@permission_classes([IsAuthenticated,])
def create_secret(request):
    try:
        data = request.data
        user = request.user
        if (("title" in data and data["title"].strip()!= "") and 
            ("secret" in data and data["secret"].strip()!= "")):
            # encrypt the secret
            encrypted = encrypt.string(data["secret"].strip())
            # save the secret
            secret_data = {"user_id": user.id, "title": data["title"], 
                           "secret": encrypted["enc_string"]}
            secret_id = create.secret(data=secret_data)
            # store encryption key in a differnt model
            key_data = {"secret_id": secret_id, "key": encrypted["key"]}
            create.enckey(data=key_data)
            return Response({"status": status.HTTP_201_CREATED,
                             "message": "Your secret has been created",
                             "data": data})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST,
                             "message": "Please provide valid data",
                             "data": {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})



@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def secret_details(request, secret_id):
    try:
        user = request.user 
        data = {}
        # check if the secret exists for this user
        secret = query.secret(secret_id, user.id)
        if secret["found"]:
            data["id"] = secret_id
            data["title"] = secret["content"]["title"]
            # decrypt the content
            encr_key = query.encr_key(secret_id)
            data["secret"] = decrypt.string(secret["content"]["secret"], encr_key["key"])
            return Response({"status": status.HTTP_200_OK,
                             "message": "Secret",
                             "data": data})
        else:
            return Response({"status": status.HTTP_404_NOT_FOUND,
                             "message": "Your secret was not found",
                             "data" : {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def edit_secret(request, secret_id):
    try:
        data  = request.data
        user = request.user
        # check if the secret exists for this user
        secret = query.secret(secret_id, user.id)
        if secret["found"]:
            # encrypt the content
            encrypted = encrypt.string(data["new_secret"].strip())
            secret_data = {"title": data["title"], "secret": encrypted["enc_string"]}
            # update the secret
            update.secret(secret_id=secret_id, data=secret_data)
            # update the corresponding key
            key_data = {"key": encrypted["key"]}
            update.enckey(secret_id=secret_id, data=key_data)
            return Response({"status": status.HTTP_201_CREATED,
                             "message": "Your secret has been updated",
                             "data": data})
        else:
            return Response({"status": status.HTTP_404_NOT_FOUND,
                             "message": "Your secret was not found",
                             "data" : {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated,])
def delete_secret(request, secret_id):
    try:
        data  = request.data
        user = request.user
        # check if the secret exists for this user
        secret = query.secret(secret_id, user.id)
        if secret["found"]:
            delete.secret(secret_id=secret_id)
            delete.enckey(secret_id=secret_id)
            return Response({"status": status.HTTP_200_OK,
                             "message": "Your secret has been deleted",
                             "data": {}})
        else:
            return Response({"status": status.HTTP_404_NOT_FOUND,
                             "message": "Your secret was not found",
                             "data" : {}})
    except:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Something went wrong",
                         "data" : {}})