import base64
import random
import uuid
from dbm import error

from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from ..models import *
from fcm_django.models import FCMDevice
from rest_framework.pagination import PageNumberPagination
from plusco.pagination import PaginationHandlerMixin


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class OrganizationView(APIView):
    def get(self, request, format=None):
        data = Organization.objects.filter(title__contains=request.GET['item']).all()
        serilizer = OrgSerilizer(data, many=True)
        return Response(serilizer.data)

    def post(self, request, format=None):
        if request.data.get('image', False):
            base64_file = request.data.pop('image')
            format, imgstr = base64_file.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + "." + ext)
            request.data['image'] = image
        data = OrgSerilizer(data=request.data)
        if data.is_valid():
            data.save(owner=request.user)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class OrgFactoryView(APIView):
    def get(self, request, pk, format=None):
        data = Factory.objects.filter(organization__exact=pk, title__contains=request.GET['item']).all()
        serilizer = FactorySerilizer(data, many=True)
        return Response(serilizer.data)


class FactoryView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def post(self, request, format=None):
        data = FactorySerilizer(data=request.data)
        if data.is_valid():
            factory = data.save(owner=request.user)
            admin_group = AdminGroup.objects.create(owner=request.user, factory=factory)
            AdminUser.objects.create(user=request.user, admin_group=admin_group)
            Department.objects.create(owner=request.user, title="HSC", factory=factory)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None, ):
        data = Factory.objects.filter(
            Q(title__contains=request.GET['item']) | Q(organization__title__contains=request.GET['item'])).all()
        data = self.paginate_queryset(data)
        if data is not None:
            serilizer = self.get_paginated_response(FactorySerilizer(data, many=True).data)
        else:
            serilizer = FactorySerilizer(data, many=True)
        return Response(serilizer.data)


class DepartmentView(APIView):
    def post(self, request, format=None):
        records = []
        for item in request.data['title']:
            request.data['title'] = item
            data = DepartmentSerilizer(data=request.data)
            if data.is_valid():
                record = data.save(owner=request.user)
                records.append(record.id)
        departments = Department.objects.filter(id__in=records)
        data = DepartmentSerilizer(departments, many=True)
        return Response(data.data, status=status.HTTP_200_OK)
        # return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        authority = UserAuthority.objects.filter(user=request.user, status_id__in=[1, 4], is_active=True).first()
        if authority == None:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        serilizer = DepartmentSerilizer(authority.department, many=False)
        return Response(serilizer.data)


class DepartmentPositioView(APIView):
    def get(self, request, pk, format=None):
        data = Position.objects.filter(department__exact=pk).all()
        serilizer = PositionSerilizer(data, many=True)
        return Response(serilizer.data)


class StatusView(APIView):
    def get(self, request, format=None):
        data = Status.objects.all()
        serilizer = StatusSerilizer(data, many=True)
        return Response(serilizer.data)


class FactoryMembersView(APIView):
    def get(self, request, format=None):
        factory = UserAuthority.objects.get(Q(user=request.user, is_active=True) & ~Q(status_id=2)).department.factory
        users = UserAuthority.objects.filter(department__factory=factory).all()
        if users:
            authority = DepartmentMemberSerilizer(users, many=True)
            return Response(authority.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, 'message': "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class DepartmentMemberByAdminView(APIView):
    def post(self, request, format=None):
        factory = UserAuthority.objects.get(user=request.user, status_id=4, is_active=True).department.factory
        if Department.objects.get(pk=request.data['department']).factory != factory:
            return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        # admin_group = AdminGroup.objects.get(factory=factory)
        # if not AdminUser.objects.filter(admin_group=admin_group, user=request.user).exists():
        #     return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.filter(mobile=request.data['mobile']).first()
        if user == None:
            user = User.objects.create_user(request.data['mobile'], random.randint(11111, 99999))
        UserAuthority.objects.filter(department__factory=Department.objects.get(pk=request.data['department']).factory,
                                     user__mobile=request.data['mobile']).delete()
        user_authority = UserAuthority.objects.create(user=user, department_id=request.data['department'],
                                                      status_id=request.data['status'],
                                                      name=request.data.get('name', None),
                                                      family=request.data.get('family', None),
                                                      national_code=request.data.get('national_code', None),
                                                      email=request.data.get('email', None),
                                                      phone=request.data.get('phone', None),
                                                      education=request.data.get('education', None),
                                                      position_id=request.data.get('position', None),

                                                      )
        return Response(DepartmentMemberSerilizer(user_authority, many=False).data)


class DepartmentSwitchView(APIView):
    def put(self, request, format=None):
        authority = UserAuthority.objects.get(pk=request.data['member_id'], user=request.user)
        for item in UserAuthority.objects.filter(user=request.user).all():
            item.is_active = False
            item.save()
        authority.is_active = True
        authority.save()
        serilizer = DepartmentMemberSerilizer(authority, many=False)
        return Response(serilizer.data, status=status.HTTP_200_OK)


class DepartmentMemberView(APIView):
    def get(self, request, format=None):
        if UserAuthority.objects.filter(user=request.user).exists():
            authority = UserAuthority.objects.filter(user=request.user).all()
            authority = DepartmentMemberSerilizer(authority, many=True)
            return Response(authority.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, 'message': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        if 'status' in request.data:
            request.data.pop('status')
        send_notif = False
        status_id = 2
        is_active = False

        dep = Department.objects.get(pk=request.data['department'])
        if UserAuthority.objects.filter(user=request.user, department__factory=dep.factory).exists():
            if UserAuthority.objects.filter(user=request.user,
                                            department__factory=dep.factory).first().department.factory == dep.factory:
                authority = UserAuthority.objects.filter(user=request.user, department__factory=dep.factory).first()
                if authority.status_id != 1 and authority.status_id != 4:
                    send_notif = True

                status_id = authority.status_id
                authority.delete()
                for item in UserAuthority.objects.filter(user=request.user, is_active=True).all():
                    item.is_active = False
                    item.save()
                is_active = True

        if dep.factory.owner == request.user:
            for item in UserAuthority.objects.filter(user=request.user, is_active=True).all():
                item.is_active = False
                item.save()
            status_id = 4
            is_active = True
        if send_notif == True:
            status_id = 2
            # admin_group = AdminGroup.objects.get(factory=Department.objects.get(pk=request.data['department']).factory)
            user_ids = UserAuthority.objects.filter(user=request.user, is_active=True, status_id=4,
                                                    department_id=request.data['department']) \
                .all().values_list('user_id', flat=True)
            # user_ids = AdminUser.objects.filter(admin_group=admin_group).all().values_list('user_id', flat=True)
            device = FCMDevice.objects.filter(user_id__in=user_ids).all()
            payload = {
                "type": "accept-user",
                "priority": "high",
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            }
            is_active = False
        request.data['user'] = str(request.user.id)
        data = DepartmentMemberSerilizer(data=request.data)
        if data.is_valid():
            data.save(status_id=status_id, is_active=is_active)
            if send_notif == True:
                device.send_message(title='تقاضای عضویت', body='یک در خواست جدید عضویت ثبت شد', data=payload)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        if UserAuthority.objects.filter(id=request.data['member_id'], user=request.user).first() == None:
            return Response({'success': False, 'message': 'دسترسی ندارد'}, status=status.HTTP_403_FORBIDDEN)
        if 'status' in request.data:
            request.data.pop('status')

        authority = UserAuthority.objects.get(id=request.data['member_id'])
        data = DepartmentMemberSerilizer(authority, data=request.data)
        if data.is_valid():
            instance = data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class NewRequestAuthorityMember(APIView):
    def get(self, request, format=None):
        # admin_group = AdminGroup.objects.get(
        #     factory=UserAuthority.objects.get(user=request.user, status_id__in=[1, 4],
        #                                       is_active=True).department.factory)
        # if not AdminUser.objects.filter(admin_group=admin_group, user=request.user).exists():
        #     return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        factory = UserAuthority.objects.get(user=request.user, status_id=4, is_active=True).department.factory
        if Department.objects.get(pk=request.data['department']).factory != factory:
            return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        else:
            new_user = UserAuthority.objects.filter(
                department=UserAuthority.objects.get(user=request.user, is_active=True).department,
                status=2).all()
            return Response(DepartmentMemberSerilizer(new_user, many=True).data)

    def post(self, request, format=None):
        factory = UserAuthority.objects.get(user=request.user, status_id=4, is_active=True).department.factory
        if Department.objects.get(pk=request.data['department']).factory != factory:
            return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        # admin_group = AdminGroup.objects.get(
        #     factory=UserAuthority.objects.get(user=request.user, status_id__in=[1, 4],
        #                                       is_active=True).department.factory)
        # if not AdminUser.objects.filter(admin_group=admin_group, user=request.user).exists():
        #     return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        else:
            user = User.objects.get(mobile__exact=request.data['mobile'])
            if factory.owner.id == user.id:
                return Response({"status": False, 'message': 'مالک کارگاه'}, status=status.HTTP_400_BAD_REQUEST)

            user_authority = UserAuthority.objects.get(pk=request.data['id'], user=user)
            device = FCMDevice.objects.filter(user=User.objects.get(mobile=request.data['mobile'])).all()
            payload = {
                "type": "get-accept-state",
                "priority": "high",
                "state": request.data['active'],
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            }
            device.send_message(title='بررسی درخواست ورود', body='درخواست شما بررسی شد', data=payload)
            if request.data['active'] == 1:
                user_authority.status_id = 1
                user_authority.save()
                return Response({'status': True, 'message': 'فعال شد'})
            else:
                admin_group = AdminGroup.objects.get(
                    factory=UserAuthority.objects.get(id=request.data['id']).department.factory)
                if AdminUser.objects.filter(admin_group=admin_group, user=user_authority.user).exists():
                    AdminUser.objects.get(admin_group=admin_group, user=user_authority.user).delete()
                user_authority.delete()
                return Response({'status': True, 'message': 'حذف شد'})


class FactoryDepartmentView(APIView):
    def get(self, request, pk, format=None):
        data = Department.objects.filter(factory__exact=pk, title__contains=request.GET['item']).all()
        serilizer = DepartmentSerilizer(data, many=True)
        return Response(serilizer.data)


class FactoryAreaView(APIView):
    def get(self, request, pk, format=None):
        data = Area.objects.filter(factory__exact=pk, title__contains=request.GET['item']).all()
        serilizer = AreaSerilizer(data, many=True)
        return Response(serilizer.data)


class AreaView(APIView):
    def post(self, request, format=None):
        data = AreaSerilizer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class PartAreaView(APIView):
    def get(self, request, pk, format=None):
        data = Part.objects.filter(area__exact=pk, title__contains=request.GET['item']).all()
        serilizer = PartSerilizer(data, many=True)
        return Response(serilizer.data)


class RelationTypeView(APIView):
    def get(self, request, format=None):
        data = RelationType.objects.all()
        serilizer = RelationTypeSerilizer(data, many=True)
        return Response(serilizer.data)


class AdminView(APIView):
    def get(self, request, format=None):
        admin_group = AdminGroup.objects.get(
            factory=UserAuthority.objects.get(user=request.user, is_active=True).department.factory)
        serilizer = AdminGroupSerilizer(admin_group, many=False)
        return Response(serilizer.data)

    def post(self, request, format=None):
        try:
            admin_group = AdminGroup.objects.get(
                factory=UserAuthority.objects.get(user=request.user, is_active=True).department.factory)
            user = User.objects.get(mobile__exact=request.data['mobile'])
            if not AdminUser.objects.filter(user=user, admin_group=admin_group).exists():
                AdminUser.objects.create(user=user, admin_group=admin_group)
            serilizer = AdminGroupSerilizer(admin_group, many=False)
            return Response(serilizer.data)
        except Exception as e:
            return Response({'status': False, "debug": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        admin_group = AdminGroup.objects.get(
            factory=UserAuthority.objects.get(user=request.user, is_active=True).department.factory)
        user = User.objects.get(mobile__exact=request.data['mobile'])
        if admin_group.owner.id == user.id:
            return Response({'status': False, "message": "مالک کارگاه"}, status=status.HTTP_400_BAD_REQUEST)
        if AdminUser.objects.filter(user=user, admin_group=admin_group).exists():
            AdminUser.objects.get(user=user, admin_group=admin_group).delete()
            return Response({'status': True, "message": "با موفقیت پاک شد"})
        return Response({'status': False, "message": "یافت نشد"}, status=status.HTTP_404_NOT_FOUND)


class RelationView(APIView):
    def get(self, request, format=None):
        authority = UserAuthority.objects.filter(user=request.user, is_active=True).first()
        if authority == None:
            return Response({'success': False, 'message': 'کارگاه فعالی یاقت نشد'})
        relation = Relation.objects.filter(source=authority.department.factory.id, status_id=1).all()
        serializers = RelationSerilizer(relation, many=True)
        data = {
            'depeartment_id': authority.department.id,
            'depeartment_name': authority.department.title,
            'factory_id': authority.department.factory.id,
            'factory_name': authority.department.factory.title,
            'org': authority.department.factory.organization.title,
            'org_id': authority.department.factory.organization.id
        }
        return Response({'dest':serializers.data,'src':data})

    def delete(self, request):
        # admin_group = AdminGroup.objects.get(
        #     factory=UserAuthority.objects.get(user=request.user, status_id__in=[1, 4],
        #                                       is_active=True).department.factory)
        # if not AdminUser.objects.filter(admin_group=admin_group, user=request.user).exists():
        #     return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        authority = UserAuthority.objects.filter(user=request.user, is_active=True, status_id=4).first()
        if authority == None:
            return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        if Relation.objects.filter(pk=request.GET['id']).exists():
            relation_obj = Relation.objects.get(pk=request.GET['id'])
            Relation.objects.get(source=relation_obj.target, target=relation_obj.source).delete()
            relation_obj.delete()
            return Response({'status': True, 'message': "Deleted"})
        return Response({"status": False, "message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):

        # admin_group = AdminGroup.objects.get(
        #     factory=UserAuthority.objects.get(user=request.user, status_id__in=[1, 4],
        #                                       is_active=True).department.factory)
        # if not AdminUser.objects.filter(admin_group=admin_group, user=request.user).exists():
        #     return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        authority = UserAuthority.objects.filter(user=request.user, is_active=True, status_id=4).first()
        if authority == None:
            return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)

        request.data['source'] = str(authority.department.factory.id)
        data = RelationSerilizer(data=request.data)
        if data.is_valid():
            instance = data.save(owner=request.user, status_id=2)
            Relation.objects.create(source=instance.target, target=instance.source,
                                    type=RelationType.objects.get(id=request.data['type']).opposite_title, status_id=2)
            admin_user = AdminUser.objects.filter(
                admin_group=AdminGroup.objects.get(factory_id=request.data['target'])).all().values_list('user_id',
                                                                                                         flat=True)
            device = FCMDevice.objects.filter(user_id__in=admin_user).all()
            payload = {
                "type": "accept-relation",
                "priority": "high",
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            }
            device.send_message(title='تقاضای ذینفع', body='یک در خواست جدید  ثبت شد', data=payload)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class NewRelationView(APIView):
    def get(self, request, format=None):
        # admin_group = AdminGroup.objects.get(
        #     factory=UserAuthority.objects.get(user=request.user, status_id__in=[1, 4],
        #                                       is_active=True).department.factory)
        # if not AdminUser.objects.filter(admin_group=admin_group, user=request.user).exists():
        #     return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        authority = UserAuthority.objects.get(user=request.user, is_active=True)
        relation = Relation.objects.filter(source=authority.department.factory.id, status_id=2)
        serializers = RelationSerilizer(relation, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        # admin_group = AdminGroup.objects.get(
        #     factory=UserAuthority.objects.get(user=request.user, status_id__in=[1, 4],
        #                                       is_active=True).department.factory)
        # if not AdminUser.objects.filter(admin_group=admin_group, user=request.user).exists():
        #     return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        if not Relation.objects.filter(pk=request.data['id'], owner=None).exists():
            return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if Relation.objects.filter(pk=request.data['id'], owner=None).first().target != UserAuthority.objects.get(
                    user=request.user, status_id=4, is_active=True).department.factory:
                return Response({"status": False, 'message': 'دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)

            relation = Relation.objects.get(pk=request.data['id'], owner=None)
            relation.owner = request.user
            relation.status_id = 1
            relation.save()
            reverce_relation = Relation.objects.get(source=relation.target, target=relation.source)
            reverce_relation.status_id = 1
            reverce_relation.save()
            return Response({"status": True, 'message': 'ارتباط با ذی نفع مورد نظر برقرار شد'})


class PartView(APIView):
    def post(self, request, format=None):
        data = PartSerilizer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class PositionView(APIView):
    def post(self, request, format=None):
        data = PositionSerilizer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
