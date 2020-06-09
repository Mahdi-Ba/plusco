from django.urls import path
from . import views
from .api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    # path('test', views.UploadView.as_view()),
    path('conformity/status/', views.StatusConformityView.as_view()),
    path('conformity/', views.ConformityView.as_view()),
    path('conformity/factory/board', views.ConformityFactoryBoardView.as_view()),
    path('conformity/my/board', views.ConformityMyBoardView.as_view()),
    path('conformity/detail/<int:pk>', views.ConformityDetailView.as_view()),
    path('action/status/', views.StatusActionView.as_view()),
    path('action/', views.ActionView.as_view()),
    path('action/reply', views.ActionReplyView.as_view()),
    path('action/detail/<int:pk>', views.ActionDetailView.as_view()),
    path('action/catch/', views.CatchActionView.as_view()),
    path('action/reject/', views.RejectActionView.as_view()),
    path('action/my/board', views.ActionMyBoardView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
