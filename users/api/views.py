from ..models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from .. import models
from rest_framework import generics

from . import serializers
from rest_framework import permissions
from django.contrib.auth import (
    login as django_login,
)
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_auth.app_settings import (
    TokenSerializer, JWTSerializer, create_token
)
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class OTPCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.OTPCreateSerializer


class ConfirmOtpAPIView(ObtainJSONWebToken):
    serializer_class = serializers.ConfirmOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, mobile, *args, **kwargs):
        """
        for post request
        give otp code and register user in site
        """
        try:
            # to get user otp raw in database (last and only of them )
            register_otp_obj = models.OTP.objects.filter(mobile=mobile).latest("create_time")
            serializer = self.serializer_class(instance=register_otp_obj, data=request.data)
            serializer.is_valid(raise_exception=True)  # validate code
            user_qs = models.User.objects.filter(mobile=mobile)

            if user_qs.exists():
                user = user_qs.first()
            else:
                user = User.objects.create_user(mobile=mobile)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except IndexError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except models.OTP.DoesNotExist:  # if OTP with this mobile number not exists
            return Response(status=status.HTTP_404_NOT_FOUND)


class CompleteRegistryUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CompleteRegistrySerializer

    def get_object(self):
        return self.request.user


class VerifyLoginWithSessionView(APIView):
    """
    check otp and login user with session or JWT
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ConfirmLoginOTPGeneralSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(VerifyLoginWithSessionView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    @staticmethod
    def get_response_serializer():
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self, mobile):
        """
        login user
        """
        self.user = models.User.objects.get(mobile=mobile)

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response

    def post(self, request, *args, **kwargs):
        """
        for post request
        check otp and login user
        """
        try:
            register_otp_obj = \
                models.OTP.objects.filter(mobile=kwargs["mobile"]).latest(
                    "id")  # to get user otp raw in database (first and only of them )
            serializer = self.serializer_class(instance=register_otp_obj, data=request.data)
            serializer.is_valid(raise_exception=True)  # validate code

            self.request = request
            self.serializer = serializer
            self.login(mobile=kwargs["mobile"])
            return self.get_response()

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, mobile):
        """
        for get request
        """
        try:
            register_otp_obj = \
                models.OTP.objects.filter(mobile=mobile).latest(
                    "id")
            serializer = self.serializer_class(instance=register_otp_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return self.request.user
