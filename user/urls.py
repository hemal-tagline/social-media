from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('signup/', RegisterUserView.as_view(), name='register'),
    path('login/', CutomObtainPairView.as_view(), name='login'),
    path('user-retrieve/', UserRetrieveUpdateDestroyview.as_view(), name='user-retrieve'),
    path('user-update/', UserRetrieveUpdateDestroyview.as_view(), name='user-update'),
    path('user-destroy/', UserRetrieveUpdateDestroyview.as_view(), name='user-destroy'),
    path('login-guest/', GuestUserView.as_view(),name="login-guest"),
    path('login-social-media/',SocialUserView.as_view(), name='login-social-media'),
    path('change-password/',ChangePasswordView.as_view(), name='change-password'),
    path('forget-password/',ForgotPasswordAPI.as_view(), name='forget-password'),
    path('get-all-user-view/',GetAllUserView.as_view(),  name='get-all-user-view'),
    path('device-register/', FcmTokenAPI.as_view(),
         name="device_fcm_register"),
    
]
