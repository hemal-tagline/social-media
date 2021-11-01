from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .serializer import RegisterUserSerializer , UserSerializer
from rest_framework.views import APIView
from rest_framework import status

def user_access_token(user, context, is_created=False):
    refresh = RefreshToken.for_user(user)
    response = {
        "access": str(refresh.access_token),
        "user": UserSerializer(user, context=context).data,
    }
    if is_created:
        response['message'] = "User created successfully."

    return Response(response)


# Create your views here.
class RegisterUserView(generics.CreateAPIView):
    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)

        if User.objects.filter(email__iexact=request.data['email']).exists():
            return Response({'error': {"email": ["Your email already register. please login with password."]}}, status=400)
        
        if serializer.is_valid():
            user = serializer.save()
            return user_access_token(user, self.get_serializer_context(), is_created=True)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)