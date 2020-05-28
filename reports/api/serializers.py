from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from ..models import *
from django.urls import reverse



class ConformitySerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    owner = serializers.ReadOnlyField(source='owner.mobile')
    owner_factory = serializers.ReadOnlyField(source='owner_factory.title')
    receiver_factory =  serializers.CharField(write_only=True)
    receiver_factory_title = serializers.ReadOnlyField(source='receiver_factory.title')
    text = serializers.CharField()
    priority = serializers.IntegerField()
    part = serializers.CharField()
    is_conformity = serializers.BooleanField()

    class Meta:
        model = Conformity
        fields = ['id', 'title','organization']


    # def create(self, validate_data):
    #     validate_data['organization'] = Organization.objects.get(pk=validate_data['organization'])
    #     data = Factory.objects.create(**validate_data)
    #     return data


