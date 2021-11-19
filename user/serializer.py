from rest_framework import serializers
from .models import ExcelFilesUpload, Post, User , MapHistory
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','device_id','device_type','provider_user_id','provider_type']
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
        print("validated_data : ",validated_data)
        return super(RegisterUserSerializer, self).create(validated_data)

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password','device_id','device_type','provider_user_id','provider_type']

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {'error': {'detail': ['No active account found with the given credentials.']}}
    }

    def validate(self, user_data):
        user_response = super(
            CustomTokenObtainPairSerializer, self).validate(user_data)

        # Access token with to include user detail.
        user_response.pop('refresh')
        user_response.update({
            "user": UserSerializer(self.user).data
        })
        return user_response
    
class GuestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'device_id', 'device_type', 'provider_type',)
        
class SocialUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name','email', 'provider_type','provider_user_id', 'device_id', 'device_type')
        extra_kwargs = {
            "email": {
                'required': True,
                'allow_blank': False,
                'validators': [
                    EmailValidator
                ]
            },
            "provider_type": {
                'required': True,
                'allow_blank': False,
            },
            "provider_user_id": {
                'required': True,
                'allow_blank': False,
            },
            "password": {'write_only': True},
        }
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Your old password was entered incorrectly. Please enter it again.'
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(make_password(password))
        user.save()
        return user

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128, required=True)
    
    def validate(self, data):
        try:
            userObj = User.objects.get(email__iexact=data['email'])
            password = User.objects.make_random_password()
            userObj.set_password(password)
            userObj.save()
            
            subject = F"Password Reset"
            message = F"{userObj} Your Password is: {password}"

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[userObj.email]
            )
            return data
        except User.DoesNotExist:
            return Response({'error': "Provided email doesn't exist."}, status=404)
        
        
class FcmTokenSerializer(serializers.Serializer):
    DEVICE_TYPE = (
        ('android', 'android'),
        ('ios', 'ios'),
    )
    registration_id = serializers.CharField(max_length=255)
    device_id = serializers.CharField(max_length=255)
    device_type = serializers.ChoiceField(choices=DEVICE_TYPE)


class MapHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MapHistory
        fields = "__all__"
        extra_kwargs = {
            "location" : {
                'required':False
            }
        }
    def create(self, validated_data):
        validated_data['location'] = f"({validated_data['destination_longitude']}, {validated_data['destination_latitude']})"
        map_history = MapHistory.objects.create(**validated_data)
        return map_history
    
class ExcelFilesUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFilesUpload
        fields = "__all__"
    
    # def create(self, validated_data):
    #     print("validated_data : ",validated_data['Files'])
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"