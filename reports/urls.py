from django.urls import path
from . import views
from .api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    # path('test', views.UploadView.as_view()),
    path('inspection/', views.InspectionView.as_view()),
    path('inspection/<int:pk>', views.InspectionView.as_view()),
    path('inspection/archive/<int:is_archive>', views.InspectionArchiveView.as_view()),
    path('inspection/update/<int:pk>', views.InspectionUpdateView.as_view()),
    path('conformity/status/', views.StatusConformityView.as_view()),
    path('conformity/', views.ConformityView.as_view()),
    path('conformity/image/<int:pk>', views.ConformityImageView.as_view()),
    path('action/list', views.ConformityView.as_view()),
    path('conformity/detail/<int:pk>', views.ConformityDetailView.as_view()),
    path('action/catch/', views.CatchActionView.as_view()),
    path('action/reject/', views.RejectActionView.as_view()),
    path('action/status/', views.StatusActionView.as_view()),
    path('action/', views.ActionView.as_view()),
    path('action/image/<int:pk>', views.ActionImageView.as_view()),

    path('conformity/change/status/<int:pk>', views.ConformityConfirmView.as_view()),
    path('action/confirm/<int:pk>', views.ActionConfirmView.as_view()),
    path('conformity/department/board', views.ConformityFactoryBoardView.as_view()),
    path('action/detail/<int:pk>', views.ActionDetailView.as_view()),
    path('conformity/my/board', views.ConformityMyBoardView.as_view()),

    path('action/my/board', views.ActionMyBoardView.as_view()),

    # remove below
    path('action/reply', views.ActionReplyView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
