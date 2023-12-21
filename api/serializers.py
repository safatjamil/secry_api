from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *
from modules.encrypt import *

encrypt = Encrypt()

class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = CustomUser
        fields = ["email", "first_name", "last_name", "password"]


class UserAuthSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
