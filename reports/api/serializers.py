from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
# from organizations.api.serializers import PartSerilizer
from organizations.api.serializers import PartSerilizer, FactorySerilizer, DepartmentSerilizer
from users.api.serializers import BriefUser
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
        fields = ['id', 'title']

class ActionSerilizer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(required=False, source='owner.mobile')
    owner_detail = BriefUser(many=False, required=False, read_only=True, source='owner')
    owner_factory = FactorySerilizer(required=False, many=False)
    execute_department = serializers.CharField(required=False)
    execute_owner = serializers.ReadOnlyField(required=False, source='execute_owner.mobile', allow_null=True)
    execute_owner_detail = BriefUser(many=False, required=False, read_only=True, source='execute_owner')
    conformity = serializers.CharField(required=False)
    conformity_id = serializers.IntegerField(source='conformity.id', read_only=True)
    title = serializers.CharField(max_length=255, required=False)
    text = serializers.CharField(max_length=1000, required=False)
    reply_text = serializers.CharField(max_length=1000, required=False)
    due_date = serializers.DateField(required=False, format="%s")
    action_gallery = ActionGallerySerilizer(read_only=True, many=True)
    status = serializers.CharField(required=False)

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
            'owner_detail', 'execute_owner_detail', 'status',
        ]

    def create(self, validate_data):
        validate_data['execute_department'] = Department.objects.get(pk=validate_data['execute_department'])
        validate_data['conformity'] = Conformity.objects.get(pk=validate_data['conformity'])
        if validate_data.get('status', False):
            validate_data['status'] = ActionStatus.objects.get(pk=validate_data['status'])
        data = Action.objects.create(**validate_data)
        return data



class ConformitySerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=False)
    inspection = serializers.CharField(required=False)
    inspection_id = serializers.IntegerField(source='inspection.id', read_only=True)
    # owner = serializers.ReadOnlyField(source='owner.mobile')
    # owner_detail = BriefUser(many=False, required=False, read_only=True, source='owner')
    # owner_factory = FactorySerilizer(required=False, many=False)
    receiver_department = serializers.CharField(write_only=True)
    receiver_department_detail = DepartmentSerilizer(required=False, many=False, source='receiver_department')
    text = serializers.CharField()
    priority = serializers.IntegerField()
    # part = serializers.CharField(write_only=True)
    status = serializers.CharField(required=False)
    # part_detail = PartSerilizer(required=False, source='part')
    is_conformity = serializers.BooleanField()
    conformity_gallery = ConformityGallerySerilizer(read_only=True, many=True)
    action = ActionSerilizer(read_only=True, many=True)
    date = serializers.DateField(required=False, format="%s", read_only=True)
    due_date = serializers.DateField(required=False, format="%s")

    # action_count = serializers.SerializerMethodField()

    class Meta:
        model = Conformity
        fields = ['id',
                  'title',
                  'text',
                  'inspection',
                  'inspection_id',
                  # 'owner',
                  # 'owner_factory',
                  'receiver_department',
                  'receiver_department_detail',
                  'priority',
                  # 'part',
                  'is_conformity'
                  # , 'part_detail'
            ,'conformity_gallery', 'action', 'status', 'date','due_date'
                  # 'owner_detail'
                  ]

    # def get_action_count(self, obj):
    #     return Action.objects.filter(conformity=obj).count()

    def create(self, validate_data):
        validate_data['receiver_department'] = Department.objects.get(pk=validate_data['receiver_department'])
        # if validate_data.get('part', False):
        #     validate_data['part'] = Part.objects.get(pk=validate_data['part'])
        if validate_data.get('status', False):
            validate_data['status'] = Status.objects.get(pk=validate_data['status'])
        data = Conformity.objects.create(**validate_data)
        return data


class ConformityBriefSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=False)
    text = serializers.CharField()
    owner = serializers.ReadOnlyField(source='inspection.owner.mobile')
    owner_detail = BriefUser(many=False, required=False, read_only=True, source='inspection.owner')
    inspection = serializers.CharField(required=False)
    inspection_id = serializers.IntegerField(source='inspection.id', read_only=True)
    receiver_department = serializers.CharField(write_only=True)
    receiver_department_detail = DepartmentSerilizer(required=False, many=False, source='receiver_department')
    priority = serializers.IntegerField()
    status = serializers.CharField(required=False)
    is_conformity = serializers.BooleanField()
    conformity_gallery = ConformityGallerySerilizer(read_only=True, many=True)
    date = serializers.DateField(required=False, format="%s", read_only=True)
    due_date = serializers.DateField(required=False, format="%s")


    # part = serializers.CharField(write_only=True)
    # part_detail = PartSerilizer(required=False, source='part')
    # action_count = serializers.SerializerMethodField()
    # owner_factory = FactorySerilizer(required=False, many=False)


    class Meta:
        model = Conformity
        fields = ['id',
                  'title',
                  'text',
                  'owner',
                  'owner_detail',
                  'receiver_department',
                  'receiver_department_detail',
                  'inspection',
                  'inspection_id',
                  'priority',
                  'is_conformity',
                  'conformity_gallery',
                  'status',
                  'date',
                  'due_date',



                  # 'owner_factory',
                  # 'part',
                  # 'part_detail',
                  # 'action_count',


                  ]

    # def get_action_count(self, obj):
    #     return Action.objects.filter(conformity=obj).count()



class InspectionSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=False)
    owner = serializers.ReadOnlyField(source='owner.mobile')
    owner_detail = BriefUser(many=False, required=False, read_only=True, source='owner')
    owner_factory = FactorySerilizer(required=False, many=False)
    receiver_factory = serializers.CharField(write_only=True, required=False)
    receiver_factory_detail = FactorySerilizer(required=False, many=False, source='receiver_factory')
    is_archive = serializers.BooleanField(required=False)
    conformity_count = serializers.SerializerMethodField()


    class Meta:
        model = Inspection
        fields = ['id',
                  'title',
                  'owner',
                  'owner_factory',
                  'receiver_factory',
                  'receiver_factory_detail',
                  'owner_detail',
                  'is_archive', 'conformity_count',
                  ]

    def get_conformity_count(self, obj):
        return Conformity.objects.filter(inspection=obj).count()

    def create(self, validate_data):
        validate_data['receiver_factory'] = Factory.objects.get(pk=validate_data['receiver_factory'])
        data = Inspection.objects.create(**validate_data)
        return data




class InspectionDetailSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=False)
    owner = serializers.ReadOnlyField(source='owner.mobile')
    owner_detail = BriefUser(many=False, required=False, read_only=True, source='owner')
    owner_factory = FactorySerilizer(required=False, many=False)
    receiver_factory = serializers.CharField(write_only=True, required=False)
    receiver_factory_detail = FactorySerilizer(required=False, many=False, source='receiver_factory')
    is_archive = serializers.BooleanField(required=False)
    conformity_count = serializers.SerializerMethodField()
    conformity = ConformityBriefSerilizer(read_only=True, many=True)


    class Meta:
        model = Inspection
        fields = ['id',
                  'title',
                  'owner',
                  'owner_factory',
                  'receiver_factory',
                  'receiver_factory_detail',
                  'owner_detail',
                  'is_archive', 'conformity_count',
                  'conformity'
                  ]

    def get_conformity_count(self, obj):
        return Conformity.objects.filter(inspection=obj).count()


