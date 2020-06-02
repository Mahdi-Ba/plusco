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
        fields = ['id', 'title', 'organization']
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


class DepartmentMemberSerilizer(serializers.ModelSerializer):
    user = serializers.CharField(required=False, validators=[UniqueValidator(queryset=UserAuthority.objects.all())])
    department = serializers.CharField(required=True)
    position = serializers.CharField(required=False)

    class Meta:
        model = UserAuthority
        fields = ['id', 'user', 'department', 'position']

    def create(self, validate_data):
        validate_data['user'] = User.objects.get(id=int(validate_data['user']))
        validate_data['department'] = Department.objects.get(pk=validate_data['department'])
        data = UserAuthority.objects.create(**validate_data)
        return data

    def update(self, instance, validated_data):
        instance.user = instance.user
        instance.department = Department.objects.get(pk=validated_data['department'])
        if validated_data.get('position', False):
            instance.position = Position.objects.get(pk=validated_data['position'])
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
        fields = ['title', 'order']


class RelationSerilizer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.mobile')
    source = serializers.CharField(write_only=True)
    target = serializers.CharField(write_only=True)
    source_title = serializers.CharField(source='source.title', read_only=True)
    target_title = FactorySerilizer(source='target', read_only=True)
    type = serializers.CharField()

    class Meta:
        model = Relation
        fields = ['id', 'owner', 'source', 'target', 'type', 'source_title', 'target_title']
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
    class Meta:
        model = AdminUser
        fields = ['user', ]


class AdminGroupSerilizer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.mobile')
    admin_user = AdminUserSerilizer(read_only=True, many=True)


    class Meta:
        model = AdminGroup
        fields = ['owner','admin_user',]

