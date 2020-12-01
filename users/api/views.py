import base64
import uuid
from random import random

import kavenegar

from . import serializers
from ..models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import views, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from django.core.files.base import ContentFile

from .. import models

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


# @permission_classes((AllowAny,))
# class NewPasswd(views.APIView):
#
#     def post(self, request):
#         mobile = request.data['mobile']
#         if len(mobile) < 10:
#             return Response({"status": False, "message": "incorrect mobile phone"}, 400)
#         mobile = "0" + mobile[-10:]
#         api_key = "4C48474D77574C4C385A7A737A48344B356A6B69726B6543717741396B32527A626C6D34774F654E5550633D"
#         api = kavenegar.KavenegarAPI(api_key)
#         new_pass = random.randint(11111, 99999)
#         params = {
#             'receptor': mobile,
#             'template': 'plasco',
#             'token': new_pass,
#             'type': 'sms',
#         }
#         response = api.verify_lookup(params)
#         if User.objects.filter(mobile=mobile):
#             u = User.objects.get(mobile=mobile)
#             u.set_password(new_pass)
#             u.expire_pass = True
#             u.save()
#         else:
#             user = User.objects.create_user(mobile, new_pass)
#         content = {"status": True}
#         return Response(content)


class CustomAuthToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        if len(request.data['mobile']) < 10:
            return Response({"status": False, "message": "incorrect mobile phone"}, 400)
        mobile = request.data['mobile']
        request.data['mobile'] = "0" + mobile[-10:]
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        res = response.data
        token = res.get('token')
        if token:
            user = jwt_decode_handler(token)
        else:
            req = request.data
            mobile = req.get('mobile')
            password = req.get('password')

            if mobile is None or password is None:
                return Response({'success': False,
                                 'message': 'Missing or incorrect credentials',
                                 'data': req},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(mobile=mobile)
                if not user.check_password(password):
                    return Response({'success': False,
                                     'message': 'Incorrect password',
                                     'data': req},
                                    status=status.HTTP_403_FORBIDDEN)
                if user.expire_pass == True:
                    user.set_password(User.objects.make_random_password())
                    user.save()
            except:
                return Response({'success': False,
                                 'message': 'User not found',
                                 'data': req},
                                status=status.HTTP_404_NOT_FOUND)

        user_model = User.objects.get(pk=user['user_id'])
        user_serlize = serializers.UserSerializer(user_model)
        user_serlize_data = user_serlize.data
        user_serlize_data['token'] = token
        return Response({'success': True, "user": user_serlize_data}, status=status.HTTP_200_OK)


class userInfo(views.APIView):
    def get(self, request):
        user = request.user
        user_serlize = serializers.UserSerializer(user)
        user_serlize_data = user_serlize.data
        return Response(user_serlize_data)


class ContactsCheck(views.APIView):
    def post(self, request):
        input_contacts = set(request.data['contacts'])
        match_contacts = set()
        result = User.objects.filter(mobile__in=input_contacts).values("mobile").all()
        for item in result:
            match_contacts.add(item['mobile'])
        diff_contact = input_contacts.difference(match_contacts)
        return Response({
            "match": match_contacts,
            'not_match': diff_contact
        })


class UserDetail(views.APIView):
    def put(self, request, pk=0, format=None):
        user = request.user
        if request.data.get('file', False):
            base64_file = request.data.pop('file')
            format, imgstr = base64_file.split(';base64,')
            ext = format.split('/')[-1]
            if user.file is not None:
                user.file.delete()
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
            else:
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
            request.data['file'] = data
        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageRemove(views.APIView):
    def delete(self, request, pk=0, format=None):
        user = request.user
        user.file.delete()
        return Response({'success': True}, status.HTTP_200_OK)
