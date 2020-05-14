from django.urls import path
from . import views
from .api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('', views.PageList.as_view()),
    path('<slug:slug>', views.PageDetail.as_view(), name='page_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
