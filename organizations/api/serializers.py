from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import *
from django.urls import reverse


class OrgSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True,
                                  validators=[UniqueValidator(queryset=Organization.objects.all())])

    class Meta:
        model = Organization
        fields = ['id', 'title']


class FactorySerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    organization = serializers.CharField()

    class Meta:
        model = Factory
        fields = ['id', 'title','organization']

    def create(self, validate_data):
        validate_data['organization'] = Organization.objects.get(pk=validate_data['organization'])
        data = Factory.objects.create(**validate_data)
        return data
