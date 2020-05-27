from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

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
        validators = [
            UniqueTogetherValidator(
                queryset=Factory.objects.all(),
                fields=('title', 'organization')
            )
        ]

    def create(self, validate_data):
        validate_data['organization'] = Organization.objects.get(pk=validate_data['organization'])
        data = Factory.objects.create(**validate_data)
        return data



class DepartmentSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    factory_title = serializers.CharField(source='factory.title',read_only=True)
    factory = serializers.CharField(write_only=True)

    class Meta:
        model = Department
        fields = ['id', 'title','factory_title','factory']
        validators = [
            UniqueTogetherValidator(
                queryset=Department.objects.all(),
                fields=['factory', 'title']
            )
        ]


    def create(self, validate_data):
        validate_data['factory'] = Factory.objects.get(pk=validate_data['factory'])
        data = Department.objects.create(**validate_data)
        return data


