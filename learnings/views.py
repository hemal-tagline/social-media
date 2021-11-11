from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from .serializer import PublisherSerializer
# # Create your views here.

# class PublisherView(generics.CreateAPIView):
#     serializer_class = PublisherSerializer
#     def post(self, request, *args,  **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)