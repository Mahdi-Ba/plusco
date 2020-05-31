from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
# from organizations.api.serializers import PartSerilizer
from organizations.api.serializers import PartSerilizer, FactorySerilizer
from ..models import *
from django.urls import reverse


class ConformityGallerySerilizer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = ConformityGallery
        fields = ['file']


class ActionGallerySerilizer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = ActionGallery
        fields = ['file']



class StatusSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['title', 'order']


class ActionSerilizer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(required=False, source='owner.mobile')
    owner_factory = FactorySerilizer(required=False, many=False)
    execute_department = serializers.CharField(required=False)
    execute_owner = serializers.ReadOnlyField(required=False, source='execute_owner.mobile',allow_null=True)
    conformity = serializers.CharField(required=False)
    conformity_id = serializers.IntegerField(source='conformity.id', read_only=True)
    title = serializers.CharField(max_length=255, required=False)
    text = serializers.CharField(max_length=1000, required=False)
    reply_text = serializers.CharField(max_length=1000, required=False)
    due_date = serializers.DateField(required=False, format="%s")
    action_gallery = ActionGallerySerilizer(read_only=True, many=True)


    class Meta:
        model = Action
        fields = [
                  'id',
                  'execute_owner',
                  'execute_department',
                  'owner',
                  'owner_factory',
                  'conformity',
                  'title',
                  'text',
                  'reply_text',
                  'due_date',
                  'conformity',
                  'conformity_id',
                  'action_gallery',
                  ]

    def create(self, validate_data):
        validate_data['execute_department'] = Department.objects.get(pk=validate_data['execute_department'])
        validate_data['conformity'] = Conformity.objects.get(pk=validate_data['conformity'])
        if validate_data.get('status', False):
            validate_data['status'] = Status.objects.get(order=validate_data['status'])
        data = Action.objects.create(**validate_data)
        return data





class ConformitySerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=False)
    owner = serializers.ReadOnlyField(source='owner.mobile')
    owner_factory = FactorySerilizer(required=False, many=False)
    receiver_factory = serializers.CharField(write_only=True)
    receiver_factory_detail = FactorySerilizer(required=False, many=False, source='receiver_factory')
    text = serializers.CharField()
    priority = serializers.IntegerField()
    part = serializers.CharField(write_only=True)
    status = serializers.CharField(required=False)
    part_detail = PartSerilizer(required=False, source='part')
    is_conformity = serializers.BooleanField()
    conformity_gallery = ConformityGallerySerilizer(read_only=True, many=True)
    action = ActionSerilizer(read_only=True, many=True)

    class Meta:
        model = Conformity
        fields = ['id',
                  'title',
                  'text',
                  'owner',
                  'owner_factory',
                  'receiver_factory',
                  'receiver_factory_detail',
                  'priority',
                  'part',
                  'is_conformity', 'part_detail', 'conformity_gallery', 'action', 'status']

    def create(self, validate_data):
        validate_data['receiver_factory'] = Factory.objects.get(pk=validate_data['receiver_factory'])
        if validate_data.get('part', False):
            validate_data['part'] = Part.objects.get(pk=validate_data['part'])
        if validate_data.get('status', False):
            validate_data['status'] = Status.objects.get(order=validate_data['status'])
        data = Conformity.objects.create(**validate_data)
        return data
