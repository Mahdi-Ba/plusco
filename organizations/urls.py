from django.urls import path
from .api import views

urlpatterns = [
    path("organizations/", views.OrganizationListAPIView.as_view(), name="organization_list"),
    path("organizations/<int:pk>/", views.OrganizationRetrieveUpdateAPIView.as_view(),
         name="organization_retrieve_update"),

    path("factories/create/existed-organization/", views.FactoryCreateByExistedOrganization.as_view(),
         name="create_factory_existed_organization"),
    path("factories/create/not-existed-organization/", views.FactoryCreateByNotExistedOrganization.as_view(),
         name="create_factory_not_existed_organization"),

    path("factories/", views.FactoryListAPIView.as_view(), name="factory_list"),
    path("factories/<int:pk>/", views.FactoryRetrieveUpdateAPIView.as_view(), name="factory_retrieve_update"),

    path("factories/<int:factory_pk>/employees/", views.EmployeeListCreateAPIView.as_view(), name="factory_add_employee"),
]
