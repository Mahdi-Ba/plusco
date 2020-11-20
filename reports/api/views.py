import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from finances.models import FactoryPlan
from organizations.models import UserAuthority
from plusco.pagination import PaginationHandlerMixin
from .serializers import *
from rest_framework import status
from ..models import *
from fcm_django.models import FCMDevice
import datetime


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class StatusConformityView(APIView):
    def get(self, request, format=None):
        data = Status.objects.all()
        serializer = StatusSerializer(data, many=True)
        return Response(serializer.data)


class StatusActionView(APIView):
    def get(self, request, format=None):
        data = ActionStatus.objects.all()
        serializer = StatusSerializer(data, many=True)
        return Response(serializer.data)


class InspectionView(APIView):
    def post(self, request, format=None):
        inspection = InspectionSerializer(data=request.data)
        if inspection.is_valid():
            authority = UserAuthority.objects.get(user=request.user, is_active=True, status_id__in=[1, 4])
            inspection_obj = inspection.save(owner=request.user, owner_factory=authority.department.factory)
            return Response(inspection.data, status=status.HTTP_200_OK)
        return Response(inspection.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None, ):
        inspection = Inspection.objects.filter(owner=request.user, pk=pk).first()
        inspection_serializer = InspectionDetailSerializer(inspection, many=False)
        return Response(inspection_serializer.data)


class InspectionArchiveView(APIView):
    def get(self, request, is_archive, format=None, ):
        inspection = Inspection.objects.filter(owner=request.user, is_archive=is_archive,
                                               owner_factory=UserAuthority.objects.get(user=request.user,
                                                                                       is_active=True,
                                                                                       status_id__in=[1,
                                                                                                      4]).department.factory
                                               ).all().order_by(
            '-id')[:50]
        inspection_serializer = InspectionSerializer(inspection, many=True)
        return Response(inspection_serializer.data)


class InspectionUpdateView(APIView):
    def put(self, request, pk, format=None):
        inspection = Inspection.objects.filter(owner=request.user, pk=pk).first()
        data = InspectionSerializer(inspection, data=request.data)
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
            serializer = self.get_paginated_response(ConformityBriefSerializer(page, many=True).data)

        else:
            serializer = ConformityBriefSerializer(conformity, many=True)

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
            serializer = self.get_paginated_response(ConformityBriefSerializer(page, many=True).data)
        else:
            serializer = ConformityBriefSerializer(conformity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConformityImageView(APIView):
    def delete(self, request, pk, format=None):
        gallery = ConformityGallery.objects.filter(conformity__inspection__owner=request.user, id=pk).first()
        if gallery == None:
            return Response({'success': False, 'message': 'شما دسترسی به این فایل ندارید'}, status.HTTP_403_FORBIDDEN)
        gallery.file.delete()
        gallery.delete()
        return Response({'success': True, 'message': 'با موفقیت حذف شد'})


class ConformityView(APIView):
    def post(self, request, format=None):
        authority = UserAuthority.objects.filter(user=request.user, is_active=True, status_id__in=[1, 4]).first()
        if authority == None:
            return Response({"status": False, 'message': "دسترسی وجود ندارد"}, status=status.HTTP_403_FORBIDDEN)

        plan = FactoryPlan.objects.filter(start_date__lte=datetime.datetime.now(), end_date__gt=datetime.datetime.now(),
                                          is_success=True, factory=authority.department.factory).order_by('id').first()
        if plan == None:
            return Response({"status": False, 'message': "بسته فعالی برای کارگاه وجود ندارد"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if Inspection.objects.filter(pk=request.data['inspection'], owner=request.user).count() == 0:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)
        files = request.data.pop('files')
        conformity = ConformitySerializer(data=request.data)
        if conformity.is_valid():
            # authority = UserAuthority.objects.get(user=request.user, is_active=True, status_id__in=[1, 4])
            conformity_obj = conformity.save()
            users = UserAuthority.objects.filter(department=conformity_obj.receiver_department, is_active=True,
                                                 status_id__in=[1, 4]).all().values_list('user', flat=True)
            device = FCMDevice.objects.filter(user_id__in=users).all()
            payload = {
                "type": "new-action",
                "id": conformity_obj.id,
                "priority": "high",
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            }
            device.send_message(title='بازرسی شد', body='عدم انطباق جدید دریافت شد ', data=payload)
            for file in files:
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
                request.data['file'] = data
                serializer = ConformityGallerySerializer(data=request.data)
                if serializer.is_valid():
                    obj = serializer.save(conformity=conformity_obj)
                    obj = serializer.save()
            return Response(conformity.data, status=status.HTTP_200_OK)
        return Response(conformity.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        user = UserAuthority.objects.filter(user=request.user, is_active=True, status_id__in=[1, 4]).first()
        if user is None:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)

        conformity = Conformity.objects.filter(receiver_department=user.department)
        if 'status' in request.GET:
            conformity = conformity.filter(status_id=request.GET['status'])
        conformity = conformity.all()
        serializer = ConformitySerializer(conformity, many=True)
        return Response(serializer.data)


class ConformityConfirmView(APIView):
    def post(self, request, pk, format=None):
        data = Conformity.objects.get(pk=pk)
        if data.inspection.owner != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)
        data.status_id = request.data['status']
        data.save()
        # auto archive
        if Conformity.objects.filter(inspection_id=data.inspection.id, status_id=1).first() is None:
            inspection = Inspection.objects.get(id=data.inspection.id)
            inspection.is_archive = True
            inspection.save()
        serializer = ConformitySerializer(data, many=False)
        return Response(serializer.data)


class ConformityDetailView(APIView):
    def get(self, request, pk, format=None):
        data = Conformity.objects.get(pk=pk)
        serializer = ConformitySerializer(data, many=False)
        return Response(serializer.data)


class ActionDetailView(APIView):
    def get(self, request, pk, format=None):
        data = Action.objects.get(pk=pk)
        serializer = ActionSerializer(data, many=False)
        return Response(serializer.data)


class CatchActionView(APIView):
    def post(self, request, format=None):
        data = Conformity.objects.get(pk=request.data['conformity'])
        if data.reporter is None:
            data.reporter = request.user
            data.save()
        serializer = ConformitySerializer(data, many=False)
        return Response(serializer.data)


class RejectActionView(APIView):
    def post(self, request, format=None):
        data = Conformity.objects.get(pk=request.data['conformity'])
        if data.reporter is not None:
            data.reporter = None
            data.save()
        serializer = ConformitySerializer(data, many=False)
        return Response(serializer.data)


class ActionMyBoardView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        action = Action.objects.filter(
            execute_owner=UserAuthority.objects.get(user=request.user, is_active=True,
                                                    status_id__in=[1, 4]).user).order_by('-id')
        page = self.paginate_queryset(action)
        if page is not None:
            serializer = self.get_paginated_response(ActionSerializer(page, many=True).data)

        else:
            serializer = ActionSerializer(action, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActionView(APIView):
    def post(self, request, format=None):
        data = Conformity.objects.get(pk=request.data['conformity'])
        authority = UserAuthority.objects.get(user=request.user, is_active=True, status_id__in=[1, 4])
        if data.receiver_department != authority.department or data.reporter != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)
        action = ActionSerializer(data=request.data)
        if action.is_valid():
            action_obj = action.save(execute_owner=request.user)
            device = FCMDevice.objects.filter(user=action_obj.conformity.inspection.owner).all()
            payload = {
                "type": "action-report",
                "id": action_obj.conformity.inspection.id,
                "priority": "high",
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            }
            device.send_message(title='انجام اقدام', body='اقدام جدید انجام شد', data=payload)
            files = request.data.pop('files')
            for file in files:
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
                request.data['file'] = data
                serializer = ActionGallerySerializer(data=request.data)
                if serializer.is_valid():
                    obj = serializer.save(action=action_obj)
                    obj = serializer.save()

            return Response(action.data, status=status.HTTP_200_OK)
        return Response(action.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionImageView(APIView):
    def delete(self, request, pk, format=None):
        gallery = ActionGallery.objects.filter(action__execute_owner=request.user, id=pk).first()
        if gallery is None:
            return Response({'success': False, 'message': 'شما دسترسی به این فایل ندارید'}, status.HTTP_403_FORBIDDEN)
        gallery.file.delete()
        gallery.delete()
        return Response({'success': True, 'message': 'با موفقیت حذف شد'})


class ActionReplyView(APIView):
    def post(self, request, format=None):
        return Response('تست نکنش تموم شده علیرضا')
        action_number = request.data.pop('action')
        if Action.objects.get(pk=action_number).execute_owner != request.user:
            return Response({"status": False, 'message': "دسترسی ندارید"}, status=status.HTTP_403_FORBIDDEN)

        files = request.data.pop('files')
        action = ActionSerializer(Action.objects.get(pk=action_number), data=request.data)
        if action.is_valid():
            action_obj = action.save()
            for file in files:
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
                request.data['file'] = data
                serializer = ActionGallerySerializer(data=request.data)
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
        return Response(ActionSerializer(action).data)
