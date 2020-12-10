from django.urls import path
from .api import views

urlpatterns = [
    path("organization/", views.OrganizationListAPIView.as_view(), name="organization_list"),
    path("organization/<int:pk>/", views.OrganizationRetrieveUpdateAPIView.as_view()),

    path("factories/existed-organization/", views.FactoryCreateByExistedOrganization.as_view(),
         name="create_factory_existed_organization"),
    path("factories/not-existed-organization/", views.FactoryCreateByNotExistedOrganization.as_view(),
         name="create_factory_not_existed_organization"),

    path("factory/", views.FactoryListAPIView.as_view()),
    path("factory/<int:pk>/", views.FactoryRetrieveUpdateAPIView.as_view())

]
