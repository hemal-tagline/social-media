from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from .models import User
from .serializer import *
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

class RegisterUserView(generics.CreateAPIView):
    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)

        if User.objects.filter(email__iexact=request.data['email']).exists():
            return Response({'error': {"email": ["Your email already register. please login with password."]}}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            user = serializer.save()
            return user_access_token(user, self.get_serializer_context(), is_created=True)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserRetrieveUpdateDestroyview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None):
        user_id = self.request.user.id
        User.objects.filter(id=user_id).delete()
        return Response({"message": [f"User {user_id} deleted successfully..!!"]}, status=status.HTTP_204_NO_CONTENT)

class CutomObtainPairView(TokenObtainPairView):
    """ Create API view for serializer class 'CustomTokenObtainPairSerializer' """
    serializer_class = CustomTokenObtainPairSerializer
    
class GuestUserView(generics.GenericAPIView):
    serializer_class = GuestUserSerializer

    def post(self, request, *args,  **kwargs):
        serializer = GuestUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        get_user = User.objects.filter(
            device_id=request.data['device_id'], provider_type='guest')
        if get_user.exists():
            return user_access_token(get_user.first(), self.get_serializer_context(), is_created=False)

        user = serializer.save()
        return user_access_token(user, self.get_serializer_context(), is_created=True)
