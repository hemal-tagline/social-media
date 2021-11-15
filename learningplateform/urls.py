from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('programs', ProgramListView.as_view()),
    path('program/<int:pk>', ProgramDeatilView.as_view()),
    path('program/courses', CourseListView.as_view()),
    path('program/course/<int:pk>', CourseDeatilView.as_view()),
]