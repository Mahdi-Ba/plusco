from django.urls import path
from .api import views

urlpatterns = [
    path("organization/list/", views.OrganizationListAPIView.as_view(), name="organization_list"),
    path("factories/existed-organization/", views.FactoryCreateByExistedOrganization.as_view(),
         name="create_factory_existed_organization")
]
