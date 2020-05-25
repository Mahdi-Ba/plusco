import base64
import uuid

from .serializers import UserSerializer
from ..models import User
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import random
from django.core import serializers as serr
from django.dispatch import receiver
from ..lib import SmsNotify

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import obtain_jwt_token, ObtainJSONWebToken

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from django.core.files.base import ContentFile

from rest_framework.authtoken.models import Token
import jwt, json


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


@permission_classes((AllowAny,))
class NewPasswd(APIView):


    def post(self, request):
        import kavenegar
        import json
        api_key = "4C48474D77574C4C385A7A737A48344B356A6B69726B6543717741396B32527A626C6D34774F654E5550633D"

        api = kavenegar.KavenegarAPI(api_key)

        new_pass = random.randint(11111, 99999)

        # params = {
        #     'receptor': request.data['mobile'],
        #     'message': "تلنتو " + "\n" + "رمز عبور: " + str(new_pass),
        # }

        # response = api.sms_send(params)

        params = {
            'receptor': request.data['mobile'],
            'template': 'plasco',
            'token': new_pass,
            'type': 'sms',
        }

        response = api.verify_lookup(params)

        # sms = SmsNotify()
        # status =sms.send(text=new_pass, receiver_number=request.data['mobile'])
        if User.objects.filter(mobile=request.data['mobile']):
            u = User.objects.get(mobile=request.data['mobile'])
            u.set_password(new_pass)
            u.expire_pass = True
            u.save()
        else:
            user = User.objects.create_user(request.data['mobile'], new_pass)
            re = user.save()
        content = {"status": True}

        # content = {'new pass': new_pass}
        return Response(content)


@permission_classes((AllowAny,))
class WhichPasswd(APIView):
    def post(self, request):
        if User.objects.filter(mobile=request.data['mobile']):
            u = User.objects.get(mobile=request.data['mobile'])
            return Response({"status": True, "otp": u.expire_pass})
        else:
            return Response({"status": True, "otp": True})


class SetPasswd(APIView):
    def post(self, request):
        if request.data['password'] == request.data['password_confirm']:
            request.user.set_password(request.data['password'])
            request.user.expire_pass = False
            request.user.save()
            return Response({'success': True, 'message': "password change correctly"})
        else:
            return Response({'success': False,
                             'message': 'Password and password_confirm not match',
                             'data': request.data},
                            status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class CustomAuthToken(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        res = response.data
        token = res.get('token')
        if token:
            user = jwt_decode_handler(token)  # aleady json - don't serialize
        else:
            req = request.data  # try and find email in request
            mobile = req.get('mobile')
            password = req.get('password')

            if mobile is None or password is None:
                return Response({'success': False,
                                 'message': 'Missing or incorrect credentials',
                                 'data': req},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(mobile=mobile)
            except:
                return Response({'success': False,
                                 'message': 'User not found',
                                 'data': req},
                                status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(password):
                return Response({'success': False,
                                 'message': 'Incorrect password',
                                 'data': req},
                                status=status.HTTP_403_FORBIDDEN)

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user = UserSerializer(user).data

        u = User.objects.get(pk=user['user_id'])
        if u.expire_pass:
            u.set_password(User.objects.make_random_password())
            u.save()

        return Response({'success': True,
                         "token": token,
                         'expire_pass': u.expire_pass,
                         # 'user_id': u.pk,
                         'mobile': u.mobile,
                         'username': u.mobile,
                         "first_name": u.first_name,
                         "last_name": u.last_name,
                         "national_code": u.national_code,
                         "birth_date": u.birth_date,
                         # "user": user,
                         "file": str(u.file),
                         "email":u.email,

                         },
                        status=status.HTTP_200_OK)

        # serializer = self.serializer_class(data=request.data,
        #                                    context={'request': request})
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # token, created = Token.objects.get_or_create(user=user)
        # return Response({
        #     'token': token.key,
        #     'user_id': user.pk,
        #     'mobile': user.mobile,
        #     "first_name": user.first_name,
        #     "last_name": user.last_name,
        #     "full_name": user.first_name+' '+user.last_name,
        #     "national_code": user.national_code,
        #     "birth_date": user.birth_date,
        #     "max_amount": user.groups.values_list('max_amount',flat = True) or 10000000
        # })


class userInfo(APIView):
    def get(self, request):
        user = request.user
        content = {
            "mobile": user.mobile,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.first_name + ' ' + user.last_name,
            "national_code": user.national_code,
            "birth_date": user.birth_date,
            "file": str(user.file),
            "email":user.email,
        }
        return Response(content)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk=0, format=None):
        # user = self.get_object(pk)
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

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class UserUpdateAPIView(generics.CreateAPIView):

#     def put(self, request, *args, **kwargs):
#         data = request.data
#         user = request.user
#         try:
#             user.first_name = request.data['first_name']
#         except NameError:
#             print("first_name needed")

#         try:
#             user.last_name = request.data['last_name']
#         except NameError:
#             print("last_name needed")

#         try:
#             user.national_code = request.data['national_code']
#         except NameError:
#             print("national_code needed")

#         try:
#             user.birth_date = request.data['birth_date']
#         except NameError:
#             print("birth_date needed")
#         user.save()

#         content = {'User data updated': "ok"}
#         return Response(content)
