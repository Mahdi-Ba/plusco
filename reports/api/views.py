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
from fcm_django.models import FCMDevice


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


class InspectionView(APIView):
    def post(self, request, format=None):
        inspection = InspectionSerilizer(data=request.data)
        if inspection.is_valid():
            authority = UserAuthority.objects.get(user=request.user, is_active=True, status_id__in=[1, 4])
            inspection_obj = inspection.save(owner=request.user, owner_factory=authority.department.factory)
            return Response(inspection.data, status=status.HTTP_200_OK)
        return Response(inspection.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None, ):
        inspection = Inspection.objects.filter(owner=request.user, pk=pk).first()
        inspection_serilizer = InspectionDetailSerilizer(inspection, many=False)
        return Response(inspection_serilizer.data)


class InspectionArchiveView(APIView):
    def get(self, request, is_archive, format=None, ):
        inspection = Inspection.objects.filter(owner=request.user, is_archive=is_archive,
                                               owner_factory=UserAuthority.objects.get(user=request.user,
                                                                                       is_active=True,
                                                                                       status_id__in=[1,
                                                                                                      4]).department.factory
                                               ).all().order_by(
            '-id')[:50]
        inspection_serilizer = InspectionSerilizer(inspection, many=True)
        return Response(inspection_serilizer.data)


class InspectionUpdateView(APIView):
    def put(self, request, pk, format=None):
        inspection = Inspection.objects.filter(owner=request.user, pk=pk).first()
        data = InspectionSerilizer(inspection, data=request.data)
        if data.is_valid():
            instance = data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class ConformityFactoryBoardView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        authority = UserAuthority.objects.get(user=request.user, is_active=True, status_id__in=[1, 4]).department
        conformity = Conformity.objects.filter(receiver_department=authority).order_by('-id')
        page = self.paginate_queryset(conformity)
        if page is not None:
            serializer = self.get_paginated_response(ConformityBriefSerilizer(page, many=True).data)

        else:
            serializer = ConformityBriefSerilizer(conformity, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ConformityMyBoardView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        conformity = Conformity.objects. \
            filter(inspection__owner=request.user,
                   inspection__owner_factory=
                   UserAuthority.objects.get(user=request.user,
                                             is_active=True,
                                             status_id__in=[1, 4]).department.factory).order_by('-id')
        page = self.paginate_queryset(conformity)
        if page is not None:
            serializer = self.get_paginated_response(ConformityBriefSerilizer(page, many=True).data)
        else:
            serializer = ConformityBriefSerilizer(conformity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConformityView(APIView):
    def post(self, request, format=None):
        if Inspection.objects.filter(pk=request.data['inspection'], owner=request.user).count() == 0:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)
        files = request.data.pop('files')
        conformity = ConformitySerilizer(data=request.data)
        if conformity.is_valid():
            authority = UserAuthority.objects.get(user=request.user, is_active=True, status_id__in=[1, 4])
            conformity_obj = conformity.save()
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
    def post(self, request, pk, format=None):
        data = Conformity.objects.get(pk=pk)
        if data.inspection.owner != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)
        data.status_id = request.data['status']
        data.save()
        # auto archive
        if Conformity.objects.filter(inspection_id=data.inspection.id, status_id=1).first() == None:
            inspection = Inspection.objects.get(id=data.inspection.id)
            inspection.is_archive = True
            inspection.save()
        serilizer = ConformitySerilizer(data, many=False)
        return Response(serilizer.data)


class ConformityDetailView(APIView):
    def get(self, request, pk, format=None):
        data = Conformity.objects.get(pk=pk)
        serilizer = ConformitySerilizer(data, many=False)
        return Response(serilizer.data)


class ActionDetailView(APIView):
    def get(self, request, pk, format=None):
        data = Action.objects.get(pk=pk)
        serilizer = ActionSerilizer(data, many=False)
        return Response(serilizer.data)


class CatchActionView(APIView):
    def post(self, request, format=None):
        data = Conformity.objects.get(pk=request.data['conformity'])
        if data.reporter == None:
            data.reporter = request.user
            data.save()
        serilizer = ConformitySerilizer(data, many=False)
        return Response(serilizer.data)


class RejectActionView(APIView):
    def post(self, request, format=None):
        data = Conformity.objects.get(pk=request.data['conformity'])
        if data.reporter != None:
            data.reporter = None
            data.save()
        serilizer = ConformitySerilizer(data, many=False)
        return Response(serilizer.data)


class ActionMyBoardView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        action = Action.objects.filter(
            execute_owner=UserAuthority.objects.get(user=request.user, is_active=True,
                                                    status_id__in=[1, 4]).user).order_by('-id')
        page = self.paginate_queryset(action)
        if page is not None:
            serializer = self.get_paginated_response(ActionSerilizer(page, many=True).data)

        else:
            serializer = ActionSerilizer(action, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActionView(APIView):
    def post(self, request, format=None):
        data = Conformity.objects.get(pk=request.data['conformity'])
        authority = UserAuthority.objects.get(user=request.user, is_active=True, status_id__in=[1, 4])
        if data.receiver_department != authority.department or data.reporter != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)
        action = ActionSerilizer(data=request.data)
        if action.is_valid():
            action_obj = action.save(execute_owner=request.user)
            files = request.data.pop('files')
            for file in files:
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
                request.data['file'] = data
                serializer = ActionGallerySerilizer(data=request.data)
                if serializer.is_valid():
                    obj = serializer.save(action=action_obj)
                    obj = serializer.save()
            # users = UserAuthority.objects.filter(department_id=request.data['execute_department']).all().values_list(
            #     'user_id', flat=True)
            # device = FCMDevice.objects.filter(user_id__in=users).all()
            # data = {
            #     "type": "action",
            #     "action_id": action_obj.id,
            #     "conformity_detail": request.data['conformity'],
            #     "priority": "high",
            #     "click_action": "FLUTTER_NOTIFICATION_CLICK"
            # }
            # device.send_message(title='اقدام', body='یک اقدام جدید ثبت شد', data=data)
            return Response(action.data, status=status.HTTP_200_OK)
        return Response(action.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionReplyView(APIView):
    def post(self, request, format=None):
        return Response('تست نکنش تموم شده علیرضا')
        action_number = request.data.pop('action')
        if Action.objects.get(pk=action_number).execute_owner != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)

        files = request.data.pop('files')
        action = ActionSerilizer(Action.objects.get(pk=action_number), data=request.data)
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
    def post(self, request, pk, format=None):
        if Action.objects.get(pk=pk).conformity.reporter != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)

        action = Action.objects.get(pk=pk)
        action.status_id = request.data['status']
        action.save()
        return Response(ActionSerilizer(action).data)
