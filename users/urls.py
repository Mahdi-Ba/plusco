from django.urls import path
from .api import views

urlpatterns = [
    path("otp/", views.OTPCreateAPIView.as_view(), name="send_otp"),  # send otp for user
    path("otp/confirm/<str:mobile>/", views.ConfirmOtpAPIView.as_view()),  # confirm otp
    path("complete-registry/", views.CompleteRegistryUpdateAPIView.as_view()),  # complete registration
    path("profile/", views.ProfileAPIView.as_view()),  # see profile and update

    path("otp/confirm/session/<str:mobile>", views.VerifyLoginWithSessionView.as_view())  # for login session

]
