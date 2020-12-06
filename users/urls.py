from django.urls import path
from .api import views

urlpatterns = [
    path("otp/", views.OTPCreateAPIView.as_view(), name="send_otp"),
    path("otp/confirm/<str:mobile>", views.ConfirmOtpAPIView.as_view()),
    path("complete-registry/", views.CompleteRegistryUpdateAPIView.as_view()),
    path("otp/confirm/session/<str:mobile>", views.VerifyLoginWithSessionView.as_view())

]
