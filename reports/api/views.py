import base64
import uuid
from fcm_django.models import FCMDevice
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from organizations.models import UserAuthority, AdminGroup, AdminUser
from plusco.pagination import PaginationHandlerMixin
from .serializers import *
from rest_framework import status
from ..models import *


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class StatusConformityView(APIView):
    def get(self, request, format=None):
        data = Status.objects.all()
        serilizer = StatusSerilizer(data, many=True)
        return Response(serilizer.data)

class StatusActionView(APIView):
    def get(self, request, format=None):
        data = ActionStatus.objects.all()
        serilizer = StatusSerilizer(data, many=True)
        return Response(serilizer.data)

class ConformityFactoryBoardView(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        authority = UserAuthority.objects.get(user=request.user).department.factory
        conformity = Conformity.objects.filter(receiver_factory=authority).order_by('-id')
        page = self.paginate_queryset(conformity)
        if page is not None:
            serializer = self.get_paginated_response(ConformityBriefSerilizer(page,many=True).data)

        else:
            serializer = ConformityBriefSerilizer(conformity, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ConformityMyBoardView(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        conformity = Conformity.objects.filter(owner=request.user).order_by('-id')
        page = self.paginate_queryset(conformity)
        if page is not None:
            serializer = self.get_paginated_response(ConformityBriefSerilizer(page,many=True).data)

        else:
            serializer = ConformityBriefSerilizer(conformity, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)





class ConformityView(APIView):
    def post(self, request, format=None):
        files = request.data.pop('files')
        conformity = ConformitySerilizer(data=request.data)
        if conformity.is_valid():
            authority = UserAuthority.objects.get(user=request.user)
            conformity_obj = conformity.save(owner=request.user,owner_factory= authority.department.factory)
            for file in files:
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
                request.data['file'] = data
                serializer = ConformityGallerySerilizer(data=request.data)
                if serializer.is_valid():
                    obj = serializer.save(conformity=conformity_obj)
                    obj = serializer.save()
            return Response(conformity.data, status=status.HTTP_200_OK)
        return Response(conformity.errors, status=status.HTTP_400_BAD_REQUEST)


class ConformityConfirmView(APIView):
    def post(self, request,pk, format=None):
        data = Conformity.objects.get(pk=pk)
        if data.owner != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)
        data.status_id = request.data['status']
        data.save()
        serilizer = ConformitySerilizer(data, many=False)
        return Response(serilizer.data)

class ConformityDetailView(APIView):
    def get(self, request,pk, format=None):
        data = Conformity.objects.get(pk=pk)
        serilizer = ConformitySerilizer(data, many=False)
        return Response(serilizer.data)

class ActionDetailView(APIView):
    def get(self, request,pk, format=None):
        data = Action.objects.get(pk=pk)
        serilizer = ActionSerilizer(data, many=False)
        return Response(serilizer.data)

class CatchActionView(APIView):
    def post(self, request, format=None):
        data = Action.objects.get(pk=request.data['action'])
        if data.execute_owner == None:
            data.execute_owner = request.user
            data.save()
        serilizer = ActionSerilizer(data, many=False)
        return Response(serilizer.data)

class RejectActionView(APIView):
    def post(self, request, format=None):
        data = Action.objects.get(pk=request.data['action'])
        if data.execute_owner != None:
            data.execute_owner = None
            data.save()
        serilizer = ActionSerilizer(data, many=False)
        return Response(serilizer.data)

class ActionMyBoardView(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        action = Action.objects.filter(execute_department=UserAuthority.objects.get(user=request.user).department).order_by('-id')
        page = self.paginate_queryset(action)
        if page is not None:
            serializer = self.get_paginated_response(ActionSerilizer(page,many=True).data)

        else:
            serializer = ActionSerilizer(action, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class ActionView(APIView):
    def post(self, request, format=None):
        # todo notif
        # admin_group = AdminGroup.objects.get(factory=Department.objects.get(pk = request.data['department']).factory)
        # AdminUser.objects.filter(admin_group=admin_group).all()
        # AdminUser.ob
        # admin_user = AdminUser.objects.filter(admin_group=AdminGroup.objects.get(factory_id=request.data['target'])).all()
        # users = UserAuthority.objects.filter(department_id=request.data['execute_department']).all()
        # device = FCMDevice.objects.filter(user_id_in=request.user.id, active=1).all()
        # device.send_message(title=request.data['title'], body=request.data['body'], data=request.data['data'])
        #
        action = ActionSerilizer(data=request.data)
        if action.is_valid():
            authority = UserAuthority.objects.get(user=request.user)
            action_obj = action.save(owner=request.user,owner_factory= authority.department.factory)
            return Response(action.data, status=status.HTTP_200_OK)
        return Response(action.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionReplyView(APIView):
    def post(self, request, format=None):
        action_number = request.data.pop('action')
        if Action.objects.get(pk=action_number).execute_owner != request.user:
            return Response({"status":False,'message':"دسترسی ندارید"},status=status.HTTP_403_FORBIDDEN)

        files = request.data.pop('files')
        action = ActionSerilizer(Action.objects.get(pk=action_number),data=request.data)
        if action.is_valid():
            action_obj = action.save()
            for file in files:
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
                request.data['file'] = data
                serializer = ActionGallerySerilizer(data=request.data)
                if serializer.is_valid():
                    obj = serializer.save(action=action_obj)
                    obj = serializer.save()
            return Response(action.data, status=status.HTTP_200_OK)
        return Response(action.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionConfirmView(APIView):
    def post(self, request,pk, format=None):
        if Action.objects.get(pk=pk).owner != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)

        action = Action.objects.get(pk=pk)
        action.status_id = request.data['status']
        action.save()
        return Response(ActionSerilizer(action).data)


