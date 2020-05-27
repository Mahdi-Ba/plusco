from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from ..models import *
from django.urls import reverse



class ConformitySerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    organization = serializers.CharField()

    class Meta:
        model = Conformity
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


