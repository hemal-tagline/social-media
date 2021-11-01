from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('signup/', RegisterUserView.as_view(), name='register'),
    path('login/', CutomObtainPairView.as_view(), name='login'),
    path('user-retrieve/', UserRetrieveUpdateDestroyview.as_view(), name='user-retrieve'),
    path('user-update/', UserRetrieveUpdateDestroyview.as_view(), name='user-update'),
    path('user-destroy/', UserRetrieveUpdateDestroyview.as_view(), name='user-destroy'),

]
