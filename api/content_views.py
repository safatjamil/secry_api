from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
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
@permission_classes([IsAuthenticated,])
def create_secret(request):
    try:
        data = request.data
        user = request.user
        
        if "title" in data and data["title"]!= "" and "secret" in data and data["secret"]!= "":
            encrypted = encrypt.string(data["secret"].strip())

            secret_data = {"user_id": user.id, "title": encrypted["title"], "secret": encrypted["enc_string"]}
            secret_id = create.secret(data = secret_data)

            key_data = {"secret_id": secret_id, "key": encrypted["key"]}
            create.enckey(data = key_data)
            
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Your secret has been updated",
                "data": {},
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