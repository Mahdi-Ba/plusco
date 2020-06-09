from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fcm_django.models import FCMDevice
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from ..models import Message
from .serializers import MessageSerializer


class TypeList(APIView):
    def get(self, request, format=None):
        return Response({'ios', 'android', 'web'})


class SendTestMessage(APIView):
    def post(self, request, format=None):
        if FCMDevice.objects.filter(user_id=request.user.id, active=1).exists():
            device = FCMDevice.objects.filter(user_id=request.user.id, active=1).all()
            device.send_message(title=request.data['title'], body=request.data['body'], data=request.data['data'])
        return Response({"success": True, "send-data": request.data})

class InboxMessages(APIView):
    def get(self, request, format=None):
        data = Message.objects.filter(user=request.user).all()
        serilizer = MessageSerializer(data,many=True)
        return Response(serilizer.data)







@permission_classes((AllowAny,))
class CronMessage(APIView):
    def post(self, request, format=None):
        try:
            now = timezone.now()
            twenty_nine_min_ago = now - timedelta(minutes=29)
            thirty_min_ago = now - timedelta(minutes=30)
            # users = str.split(options['userId'][0], ',')
            users_query = User.objects.filter(say_hi=False, date_joined__lt=str(twenty_nine_min_ago),
                                              date_joined__gte=str(thirty_min_ago)).all()
            users = users_query.all()
            for user in users:
                if FCMDevice.objects.filter(user_id=user.id, active=1).exists():
                    device = FCMDevice.objects.filter(user_id=user.id, active=1).all()
                    payload = {
                        "header": "خوش آمدید",
                        "description": "ورود شما را به خانواده گردش پی خوش آمد میگوییم",
                        "priority": "high",
                    }
                    device.send_message(title='خوش آمدید', body='ورود شما را به خانواده گردش پی خوش آمد میگوییم',data=payload)
            users_query.update(say_hi=True)
            return Response({"status": True})
        except Exception:
            return Response({"status": False})
