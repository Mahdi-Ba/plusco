from ..models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(max_length=200, required=False)
    last_name = serializers.CharField(max_length=200, required=False)
    national_code = serializers.CharField(max_length=200, required=False,allow_blank=True)
    birth_date = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    mobile = serializers.CharField(read_only=False, required=False)
    file = serializers.ImageField(required=False, allow_null=True)
    expire_pass = serializers.BooleanField(required=False)
    trusted = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['id','mobile', 'first_name', 'last_name', 'national_code', 'password', 'expire_pass', 'birth_date', 'file','trusted']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.national_code = validated_data.get('national_code', instance.national_code)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance


class BriefUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','mobile', 'first_name', 'last_name','file']
