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
    path('status/member', views.StatusView.as_view(), name=None),
    path('factory/members', views.FactoryMembersView.as_view(), name=None),
    path('department/member', views.DepartmentMemberView.as_view(), name=None),
    path('department/member/follower', views.NewRequestAuthorityMember.as_view(), name=None),
    path('department/<int:pk>/position', views.DepartmentPositioView.as_view(), name=None),
    path('factory/<int:pk>/area', views.FactoryAreaView.as_view(), name=None),
    path('area/', views.AreaView.as_view(), name=None),
    path('area/<int:pk>/part', views.PartAreaView.as_view(), name=None),
    path('part/', views.PartView.as_view(), name=None),
    path('position/', views.PositionView.as_view(), name=None),
    path('relation/type', views.RelationTypeView.as_view(), name=None),
    path('relation/', views.RelationView.as_view(), name=None),
    path('newrelation/', views.NewRelationView.as_view(), name=None),
    path('admin/', views.AdminView.as_view(), name=None),

]

