from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):

        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


# class UserSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(min_length = 6, max_length = 100)
    
#     class Meta:
#         model = User
#         fields = ["email", "first_name", "last_name", "password"]