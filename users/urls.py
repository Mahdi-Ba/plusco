from django.urls import path
from . import views
from .api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token



urlpatterns = [
    path('passwd/', views.NewPasswd.as_view(), name=None),
    path('set-passwd/', views.SetPasswd.as_view(), name=None),
    path('which-passwd/', views.WhichPasswd.as_view(), name=None),
    path('user-info/', views.userInfo.as_view(), name=None),
    path('contacts-check/', views.ContactsCheck.as_view(), name=None),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('update/', views.UserDetail.as_view(), name='update'),
    path('detail/<int:pk>/', views.UserDetail.as_view()),
]