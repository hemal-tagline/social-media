from rest_framework import generics, status , views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from .models import MapHistory, User
from push_notifications.models import APNSDevice, GCMDevice, WNSDevice , WebPushDevice
from .serializer import *
from rest_framework.pagination import PageNumberPagination

def user_access_token(user, context, is_created=False):
    refresh = RefreshToken.for_user(user)
    response = {
        "access": str(refresh.access_token),
        "user": UserSerializer(user, context=context).data,
    }
    if is_created:
        response['message'] = "User created successfully."

    return Response(response)

class TalentSearchpagination(PageNumberPagination):
    page_size = 2

class GetAllUserView(generics.ListAPIView):
    pagination_class = TalentSearchpagination
    serializer_class = AllUserSerializer

    def get_queryset(self):
        TalentSearch = User.objects.all()
        return TalentSearch
    
class RegisterUserView(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

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
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data)
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
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        get_user = User.objects.filter(
            device_id=request.data['device_id'], provider_type='guest')
        if get_user.exists():
            return user_access_token(get_user.first(), self.get_serializer_context(), is_created=False)

        user = serializer.save()
        return user_access_token(user, self.get_serializer_context(), is_created=True)

class SocialUserView(generics.GenericAPIView):
    serializer_class = SocialUserSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        get_user = User.objects.filter(
            Q(email__iexact=request.data['email']) | (Q(email__isnull=True) & ~Q(provider_type='guest') & Q(device_id=request.data['device_id'])))

        if get_user.exists():
            get_user.update(**serializer.data)
            return user_access_token(get_user.first(), self.get_serializer_context(), is_created=False)

        user = serializer.save()
        return user_access_token(user, self.get_serializer_context(), is_created=True)

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() 
  
        return Response({'password-change': "Password change successfully"}, status=status.HTTP_200_OK)
    
class ForgotPasswordAPI(generics.CreateAPIView):
    serializer_class = ForgetPasswordSerializer
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        '''If You are not used serializer '''
        # try:
        #     userObj = User.objects.get(email__iexact=request.data['email'])
        #     password = User.objects.make_random_password()
        #     userObj.set_password(password)
        #     userObj.save()
            
        #     subject = F"Password Reset - Demp App"
        #     message = F"{userObj} Your Temparary Password is: {password}"

        #     send_mail(
        #         subject=subject,
        #         message=message,
        #         from_email=settings.DEFAULT_FROM_EMAIL,
        #         recipient_list=[userObj]
        #     )
        #     return Response({'status': True})
        # except User.DoesNotExist:
        #     return Response({'error': "Provided email doesn't exist."}, status=404)
    
class FcmTokenAPI(generics.CreateAPIView):
    serializer_class = FcmTokenSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        fcm_data = serializer.data
        user = self.request.user

        defaults = {
            'registration_id': fcm_data['registration_id']
        }
        if self.request.user.id:
            defaults['user'] = self.request.user
            print(defaults['user'])

        try:
            if fcm_data['device_type'] == "ios":
                APNSDevice.objects.update_or_create(device_id=fcm_data['device_id'], defaults=defaults)
            elif fcm_data['device_type'] == "android":
                GCMDevice.objects.update_or_create(device_id=fcm_data['device_id'], cloud_message_type='FCM', defaults=defaults)
            elif fcm_data['device_type'] == "windows":
                WNSDevice.objects.update_or_create(device_id=fcm_data['device_id'], cloud_message_type='FCM', defaults=defaults)
        except:
            return Response({'error': {'device_id': ['device id is invalid']}}, status=400)

        return Response(serializer.data)
class MapHistoryView(views.APIView):
    def get(self, request, format=None):
        queryset = MapHistory.objects.all()
        serializer = MapHistorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = MapHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)