from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from users.api.serializers import BriefUser
from ..models import *
from django.urls import reverse


class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class PlanSerilizer(serializers.ModelSerializer):
    category = serializers.CharField()
    class Meta:
        model = Plan
        exclude = ('is_free',)

class FactoryPlanSerilizer(serializers.ModelSerializer):
    class Meta:
        model = FactoryPlan
        fields = '__all__'