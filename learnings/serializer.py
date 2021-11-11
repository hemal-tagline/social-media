from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
# from .models import Author , Publisher , Details


# class PublisherSerializer(serializers.Serializer):
#     class Meta:
#         model = Publisher
#         fields = ['publisher_name']
        
#     extra_kwargs = {
#         "publisher_name": {'required': True},
#     }
        
#     def create(self, validated_data):
#         return Publisher.objects.create(**validated_data)