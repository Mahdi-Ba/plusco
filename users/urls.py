from django.urls import path
from .api import views

urlpatterns = [
    path("otp/", views.OTPCreateAPIView.as_view(), name="send_otp"),
    path("otp/confirm/<str:mobile>",views.ConfirmOtpAPIView.as_view()),
    # path('passwd/', views.NewPasswd.as_view(), name=None),
    path('user-info/', views.userInfo.as_view(), name=None),
    path('contacts-check/', views.ContactsCheck.as_view(), name=None),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('update/', views.UserDetail.as_view(), name='update'),
    path('remove/image', views.ImageRemove.as_view(), name='update'),
    path('detail/<int:pk>/', views.UserDetail.as_view()),
]
