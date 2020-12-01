from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from .. import models, utils

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(max_length=200, required=False)
    last_name = serializers.CharField(max_length=200, required=False)
    national_code = serializers.CharField(max_length=200, required=False, allow_blank=True)
    birth_date = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    mobile = serializers.CharField(read_only=False, required=False)
    file = serializers.ImageField(required=False, allow_null=True)
    expire_pass = serializers.BooleanField(required=False)
    trusted = serializers.BooleanField(required=False)

    class Meta:
        model = models.User
        fields = ['id', 'mobile', 'first_name', 'last_name', 'national_code', 'password', 'expire_pass', 'birth_date',
                  'file', 'trusted']

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
        model = models.User
        fields = ['id', 'mobile', 'first_name', 'last_name', 'file']


class OTPCreateSerializer(ModelSerializer):
    phone_regex = RegexValidator(regex=r'^\d+$', message="مقدار معتبر وارد کنید")
    mobile = serializers.CharField(required=True, validators=[phone_regex])

    class Meta:
        model = models.OTP
        fields = ["mobile"]

    @staticmethod
    def validate_mobile(mobile):
        """
        validate mobile number
        if otp with this mobile number expired raise validation error
        """

        if len(str(mobile)) != 10 or str(mobile)[0] != "9":
            raise ValidationError("قالب شماره‌‌ی موبایل نادرست می‌‌باشد")  # if format of mobile is wrong

        otp_qs = models.OTP.objects.filter(mobile=mobile)  # OTP raw for this mobile number
        # if exists otp for this mobile number and  not expired yet raise validation error
        if otp_qs.exists():
            otp_obj = otp_qs.order_by("-id").first()
            if not otp_obj.expired:
                raise ValidationError(
                    "کد تایید شما هنوز معتبر است و قبل از منقضی شدن آن انجام چنین عملیاتی وجود ندارد",
                    code="constraint2minutes")

        return mobile

    def create(self, validated_data):
        """
        create register otp and send it with sms
        otp hashed and save in database
        """
        otp_code = utils.create_random_otp()  # make random code for OTP
        validated_data["otp"] = make_password(otp_code)  # hash otp code
        otp_instance = super(OTPCreateSerializer, self).create(
            validated_data=validated_data)  # an instance of OTP model
        utils.send_otp(mobile=otp_instance.mobile, otp=otp_code)
        return otp_instance


class ConfirmOTPSerializer(Serializer):
    otp = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(ConfirmOTPSerializer, self).__init__(*args, **kwargs)

    def validate_otp(self, otp):
        """
        validate input otp
        if otp is expired or otp is wrong , raised validation error
        """
        if self.instance.expired:  # if otp expired send error
            raise ValidationError("کد منقضی شده است")

        # elif self.instance.otp != make_password(attrs["otp"], salt="my_salt"):  # if otp not correct send error
        elif not check_password(otp, self.instance.otp):  # if otp not correct send error
            raise ValidationError("کد نادرست است")

        return otp

    def to_representation(self, instance):
        # PROPOSED  do better and put a field for token
        user = models.User.objects.filter(mobile=instance.mobile).first()

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)

            payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': {
                    'mobile': user.mobile,
                    'is_complete_registered': user.is_complete_registered
                }
            }
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)


class CompleteRegistrySerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "avatar"]
