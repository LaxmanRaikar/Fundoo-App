from rest_framework import serializers

from .models import UserProfileInfo
from . import models


class UserSerializer(serializers.ModelSerializer):  # class of User Serializer
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:                          # gives the information about the User serializer
        model = UserProfileInfo
        fields = ('username', 'password',)  # fields of a  username and password


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    email = serializers.RegexField(regex=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                   required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = UserProfileInfo
        fields = ('username', 'email', 'password',)     # fields of username,email and password















