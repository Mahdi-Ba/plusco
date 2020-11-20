from rest_framework import serializers
from organizations.api.serializers import FactorySerializer
from users.api.serializers import BriefUser
from ..models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class PlanSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Plan
        exclude = ('is_free',)


class FactoryPlanSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    user_detail = BriefUser(many=False, required=False, read_only=True, source='user')
    factory = FactorySerializer(required=False, many=False)

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
