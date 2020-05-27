from django.urls import path
from . import views
from .api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('org/', views.OrganizationView.as_view(), name=None),
    path('org/<int:pk>/factory', views.OrgFactoryView.as_view(), name=None),
    path('factory/', views.FactoryView.as_view(), name=None),
    path('factory/<int:pk>/department', views.FactoryDepartmentView.as_view(), name=None),
    path('department/', views.DepartmentView.as_view(), name=None),
    path('factory/<int:pk>/area', views.FactoryAreaView.as_view(), name=None),
    path('area/', views.AreaView.as_view(), name=None),
    path('area/<int:pk>/part', views.PartAreaView.as_view(), name=None),
    path('part/', views.PartView.as_view(), name=None),

]

