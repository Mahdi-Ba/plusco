from rest_framework import serializers
from rest_framework.fields import empty
from .. import models
from users.models import User


class ModelSerializer(serializers.ModelSerializer):
    """
    overwrite serializer.ModelSerializer for customize some thing it
    """

    def __init__(self, instance=None, data=empty, **kwargs):
        super(ModelSerializer, self).__init__(instance, data, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages.update({
                "blank": "این فیلد الزامی است",
                "null": "این فیلد الزامی است",
                "required": "این فیلد الزامی است",
                "invalid": "قالب این فیلد صحیح نمی‌باشد",
                "max_length": "اندازه‌ی این ورودی طولانی است",
                "min_length": "اندازه‌ی این ورودی کوچک است.",
            }
            )


class Serializer(serializers.Serializer):
    """
    overwrite Serializer with farsi error
    """

    def __init__(self, instance=None, data=empty, **kwargs):
        super(Serializer, self).__init__(instance, data, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages.update({
                "blank": "این فیلد الزامی است",
                "null": "این فیلد الزامی است",
                "required": "این فیلد الزامی است",
                "invalid": "قالب این فیلد صحیح نمی‌باشد",
                "max_length": "اندازه‌ی این ورودی طولانی است",
                "min_length": "اندازه‌ی این ورودی کوچک است.",
            }
            )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserSerializer(ModelSerializer):
    """
    User Serializer for this app
    """

    class Meta:
        model = User
        fields = ["id", "avatar", "first_name", "last_name"]


class OrganizationSerializer(ModelSerializer):
    """
    Organization Serializer
    """

    class Meta:
        model = models.Organization
        fields = ["id", "complete_name", "short_name", "logo"]


class EmployeeOfCompanyRetrieveSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Employee
        fields = ["id", "user", "job_title", "is_admin", "use_license"]


class GroupOfFactorySerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ["id", "name"]


class FactoryRetrieveSerializer(ModelSerializer):
    """
    Factory Retrieve Serializer
    """
    organization = OrganizationSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    employees = EmployeeOfCompanyRetrieveSerializer(many=True, read_only=True)
    groups = GroupOfFactorySerializer(many=True, read_only=True)

    class Meta:
        model = models.Factory
        fields = ["id", "organization", "name", "is_central_office", "creator", "employees", "groups"]


class FactoryCreateSerializer(ModelSerializer):
    class Meta:
        model = models.Factory
        fields = ["organization", "name", "is_central_office"]

    def to_representation(self, instance):
        return FactoryRetrieveSerializer(context=self.context).to_representation(instance=instance)


class JobTitleSerializer(ModelSerializer):
    class Meta:
        model = models.JobTitle
        fields = ["id", "title"]


class CreateNewFactoryByExistedOrganization(Serializer):
    factory = FactoryCreateSerializer()
    group_name = serializers.CharField()
    job_title = serializers.CharField()

    @staticmethod
    def validate_job_title(job_title):
        job_title_qs = models.JobTitle.objects.filter(title=str(job_title).strip())
        if job_title_qs.exists():
            return job_title_qs.first()
        else:
            job_title_serializer = JobTitleSerializer(data={"title": job_title})
            job_title_serializer.is_valid(raise_exception=True)
            job_title = job_title_serializer.save()
            return job_title

    def create(self, validated_data):
        factory_data = validated_data["factory"].copy()
        factory_data["creator"] = validated_data["creator"]
        factory = models.Factory.objects.create(**factory_data)
        group = models.Group.objects.create(name=validated_data["group_name"])
        employee = models.Employee.objects.create(factory=factory, user=validated_data["creator"],
                                                  job_title=validated_data["job_title"], is_admin=True,
                                                  use_license=True)
        group.employees.add(employee)
        return factory

    def to_representation(self, instance):
        return FactoryCreateSerializer(context=self.context).to_representation(instance=instance)
