from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from organizations.api.serializers import FactorySerilizer
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
    user = serializers.CharField(required=False)
    user_detail = BriefUser(many=False, required=False, read_only=True, source='user')
    factory = FactorySerilizer(required=False, many=False)
    class Meta:
        model = FactoryPlan
        fields = [
            'factory',
            'user',
            'user_detail',
            'count',
            'start_date',
            'end_date',
            'price',
            'percent',
            'price_with_tax',
            'is_success',
            'ref_id',

        ]