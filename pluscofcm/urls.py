from django.conf.urls import url
from django.urls import path
from .api import views
from rest_framework.urlpatterns import format_suffix_patterns
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    url(r'^devices?$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    path('type', views.TypeList.as_view()),
    path('send-message', views.SendTestMessage.as_view()),
    # path('cron-message',views.CronMessage.as_view()),
    path('inbox/messages', views.InboxMessages.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
