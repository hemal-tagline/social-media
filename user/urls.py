from django.conf.urls import url
from django.urls import path, include
from .views import RegisterUserView 
urlpatterns = [
    path('signup/', RegisterUserView.as_view(), name='normal_register'),
]
