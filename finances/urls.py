from django.urls import path
from django.conf.urls import url

from . import views
from .api import views
from .views import send_request,verify
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('category', views.CategoryView.as_view(), name=None),
    path('plan/<int:pk>', views.PlanView.as_view(), name=None),
    path('plan/reserv', views.ReservPlanView.as_view(), name=None),
    path('plan/now', views.NowPlanView.as_view(), name=None),
    path('plans/factory', views.FactoryPlanView.as_view(), name=None),
    path('plans/me', views.MePlanView.as_view(), name=None),
    url(r'^request/$', send_request, name='request'),
    url(r'^verify/$', verify, name='verify'),

]

