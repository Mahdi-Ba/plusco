from django.urls import path
from . import views
from .api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('category', views.CategoryView.as_view(), name=None),
    path('plan/<int:pk>', views.PlanView.as_view(), name=None),
    path('plan/reserv', views.ReservPlanView.as_view(), name=None),
    path('plan/now', views.NowPlanView.as_view(), name=None),
    path('plans/factory', views.FactoryPlanView.as_view(), name=None),
    path('plans/me', views.MePlanView.as_view(), name=None),

]

