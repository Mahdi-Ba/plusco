from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from users.api.serializers import BriefUser
from ..models import *
from django.urls import reverse


class OrgSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True,
                                  validators=[UniqueValidator(queryset=Organization.objects.all())])
    image = serializers.FileField(required=False)
    province = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    phone = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Organization
        fields = ['id', 'title', 'image', 'province', 'city', 'phone']


class FactorySerilizer(serializers.ModelSerializer):
    owner = BriefUser(many=False, required=False, read_only=True)
    title = serializers.CharField(max_length=255, required=True)
    organization = serializers.CharField()
    org_image = serializers.ImageField(source='organization.image', required=False, read_only=True)
    province = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    address = serializers.CharField(required=False)
    phone = serializers.CharField(max_length=255, required=False)
    rel_phone = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Factory
        fields = ['id', 'owner', 'title', 'organization', 'org_image', 'province', 'city', 'address', 'phone',
                  'rel_phone',
                  ]
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
    factory_title = serializers.CharField(source='factory.title', read_only=True)
    factory = serializers.CharField(write_only=True)

    class Meta:
        model = Department
        fields = ['id', 'title', 'factory_title', 'factory']
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


class StatusSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'title']


class DepartmentMemberSerilizer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    user_detail = BriefUser(many=False, required=False, read_only=True, source='user')
    department = serializers.CharField(required=False)
    position = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    status_title = serializers.CharField(read_only=True, source='status')
    status_item = serializers.IntegerField(required=False, write_only=True, source='status')
    factory = FactorySerilizer(read_only=True, required=False, source='department.factory')
    is_active = serializers.BooleanField(required=False)
    name = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    family = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    national_code = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    email = serializers.EmailField(required=False,allow_blank=True,allow_null=True)
    phone = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    education = serializers.CharField(required=False,allow_blank=True,allow_null=True)

    class Meta:
        model = UserAuthority
        fields = ['id', 'user', 'user_detail', 'department', 'position', 'status', 'status_title', 'factory',
                  'status_item', 'is_active', 'name', 'family', 'national_code', 'email', 'phone', 'education',
                  ]

    def create(self, validate_data):
        validate_data['user'] = User.objects.get(id=int(validate_data['user']))
        validate_data['department'] = Department.objects.get(pk=validate_data['department'])
        if validate_data.get('position', False):
            validate_data['position'] = Position.objects.get(pk=validate_data['position'])
        data = UserAuthority.objects.create(**validate_data)
        return data

    def update(self, instance, validated_data):
        instance.user = instance.user
        if validated_data.get('status', False):
            instance.status_id = validated_data['status']
        if validated_data.get('position', False):
            instance.position = Position.objects.get(pk=validated_data['position'])
        instance.name = validated_data.get('name', instance.name)
        instance.family = validated_data.get('family', instance.family)
        instance.national_code = validated_data.get('national_code', instance.national_code)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.education = validated_data.get('education', instance.education)
        instance.save()
        return instance


class AreaSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    factory_title = serializers.CharField(source='factory.title', read_only=True)
    factory = serializers.CharField(write_only=True)

    class Meta:
        model = Area
        fields = ['id', 'title', 'factory_title', 'factory']
        validators = [
            UniqueTogetherValidator(
                queryset=Area.objects.all(),
                fields=['factory', 'title']
            )
        ]

    def create(self, validate_data):
        validate_data['factory'] = Factory.objects.get(pk=validate_data['factory'])
        data = Area.objects.create(**validate_data)
        return data


class PartSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    area = serializers.CharField()

    class Meta:
        model = Part
        fields = ['id', 'title', 'area']
        validators = [
            UniqueTogetherValidator(
                queryset=Part.objects.all(),
                fields=['area', 'title']
            )
        ]

    def create(self, validate_data):
        validate_data['area'] = Area.objects.get(pk=validate_data['area'])
        data = Part.objects.create(**validate_data)
        return data


class PositionSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    department = serializers.CharField()

    class Meta:
        model = Position
        fields = ['id', 'title', 'department']
        validators = [
            UniqueTogetherValidator(
                queryset=Position.objects.all(),
                fields=['department', 'title']
            )
        ]

    def create(self, validate_data):
        validate_data['department'] = Department.objects.get(pk=validate_data['department'])
        data = Position.objects.create(**validate_data)
        return data


class RelationTypeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = RelationType
        fields = ['id', 'title', ]


class RelationSerilizer(serializers.ModelSerializer):
    owner = BriefUser(many=False, required=False, read_only=True)
    source = serializers.CharField(write_only=True)
    target = serializers.CharField(write_only=True)
    target_factory = FactorySerilizer(source='target', read_only=True)
    type = serializers.CharField()
    status_title = serializers.CharField(read_only=True, source='status')

    class Meta:
        model = Relation
        fields = ['id', 'owner', 'source', 'target', 'type', 'target_factory', 'status',
                  'status_title']
        validators = [
            UniqueTogetherValidator(
                queryset=Relation.objects.all(),
                fields=['source', 'target']
            )
        ]

    def create(self, validate_data):
        validate_data['source'] = Factory.objects.get(pk=int(validate_data['source']))
        validate_data['target'] = Factory.objects.get(pk=validate_data['target'])
        validate_data['type'] = RelationType.objects.get(pk=validate_data['type'])
        data = Relation.objects.create(**validate_data)
        return data


class AdminUserSerilizer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.mobile')
    user_detail = BriefUser(many=False, required=False, read_only=True, source='user')

    class Meta:
        model = AdminUser
        fields = ['user', 'user_detail']


class AdminGroupSerilizer(serializers.ModelSerializer):
    owner_detail = BriefUser(many=False, required=False, read_only=True, source='owner')
    owner = serializers.ReadOnlyField(source='owner.mobile')
    admin_user = AdminUserSerilizer(read_only=True, many=True)

    class Meta:
        model = AdminGroup
        fields = ['owner', 'admin_user', 'owner_detail']
