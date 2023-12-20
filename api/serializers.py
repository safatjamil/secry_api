from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *
from modules.encrypt import *

encrypt = Encrypt()

class UserSerializer(serializers.ModelSerializer):

    def validate_password(self, password: str) -> str:
        return encrypt.hash_password(password)

    class Meta(object):
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserAuthSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
