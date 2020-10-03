import base64
import datetime
import random
import uuid
from dbm import error

from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import Http404
from future.backports.datetime import timedelta
from pytz import utc
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from organizations.models import UserAuthority
from .serializers import *
from rest_framework import status
from ..models import *
from fcm_django.models import FCMDevice

from ..views import send_request


class CategoryView(APIView):
    def get(self, request, format=None):
        data = Category.objects.all()
        serilizer = CategorySerilizer(data, many=True)
        return Response(serilizer.data)


class PlanView(APIView):
    def get(self, request, pk, format=None):
        data = Plan.objects.filter(category_id=pk, is_free=False).all()
        serilizer = PlanSerilizer(data, many=True)
        return Response(serilizer.data)


class NowPlanView(APIView):
    def get(self, request, format=None):
        factory = UserAuthority.objects.get(user=request.user, is_active=True).department.factory
        data = FactoryPlan.objects.filter(start_date__lte=datetime.datetime.now(), end_date__gt=datetime.datetime.now(),
                                          is_success=True, factory=factory).order_by('id').first()
        if data == None:
            return Response({
                'success':False,
                'message':'not found'
            },status.HTTP_404_NOT_FOUND)
        serilizer = FactoryPlanSerilizer(data, many=False)
        return Response(serilizer.data)


class FactoryPlanView(APIView):
    def get(self, request, format=None):
        factory = UserAuthority.objects.get(user=request.user, is_active=True).department.factory
        data = FactoryPlan.objects.filter(factory=factory).order_by('-id').all()
        serilizer = FactoryPlanSerilizer(data, many=True)
        return Response(serilizer.data)


class MePlanView(APIView):
    def get(self, request, format=None):
        data = FactoryPlan.objects.filter(user=request.user).order_by('-id').all()
        serilizer = FactoryPlanSerilizer(data, many=True)
        return Response(serilizer.data)


class ReservPlanView(APIView):
    def post(self, request, format=None):
        factory = UserAuthority.objects.get(user=request.user, is_active=True).department.factory
        any_paln = False
        plan = Plan.objects.filter(id=request.data['plan_id'], is_free=False).first()
        if plan == None:
            return Response({'success': False, 'message': 'نبود پلن'}, status=status.HTTP_400_BAD_REQUEST)
        start_time = datetime.datetime.now()
        # TODO factory id =1 change
        factory_plan = FactoryPlan.objects.filter(factory=factory, is_success=True).last()
        if factory_plan != None:
            if start_time.replace(tzinfo=None) < factory_plan.end_date.replace(tzinfo=None):
                start_time = factory_plan.end_date
            else:
                any_paln = True
                message = 'فاقد بسته فعال برای اضافه شدن نفر'
        if plan.month != 0:
            end_time = start_time + datetime.timedelta(days=plan.month * 30)

            buy_plan = FactoryPlan.objects.create(
                factory=factory, user=request.user, count=plan.count,
                start_date=start_time, end_date=end_time,
                price=plan.price,
                percent=plan.percent,
                price_with_tax=plan.price_with_tax
            )
            data = send_request(buy_plan)
            if data[0]:
                return Response({'success': True, 'url': data[1]})
            else:
                return Response({'success':False,'message':'gateway error'})

        else:
            if any_paln:
                return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                factory_plan.increase_count = plan.count
                factory_plan.save()
                data = send_request(factory_plan)
                if data[0]:
                    return Response({'success': True, 'url': data[1]})
