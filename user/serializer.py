from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        extra_kwargs = {
            "email": {
                'required': True,
                'allow_blank': False,
                'validators': [
                    EmailValidator
                ]
            },
            "first_name": {
                'required': True,
                'allow_blank': False,
            },
            "last_name": {
                'required': True,
                'allow_blank': False,
            },
            "password": {
                'write_only': True
            },
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterUserSerializer, self).create(validated_data)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password']

    # def update(self, instance, validated_data):
    #     if 'password' in validated_data:
    #         validated_data['password'] = make_password(
    #             validated_data['password'])
    #     return super(UserSerializer, self).update(instance, validated_data)
