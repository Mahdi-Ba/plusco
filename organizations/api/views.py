from rest_framework import views, generics, permissions
from rest_framework.response import Response
from . import serializers
from .. import models, permissions as custom_permissions
from rest_framework import status


class OrganizationListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()


class OrganizationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, custom_permissions.CanEditOrganization]
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return models.Organization.objects.all()

        else:
            models.Organization.objects.filter(creator=self.request.user)


class FactoryCreateByExistedOrganization(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CreateNewFactoryByExistedOrganization

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FactoryCreateByNotExistedOrganization(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CreateNewFactoryByNotExistedOrganization

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FactoryListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.FactorySerializer
    queryset = models.Factory.objects.all()


class FactoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.FactoryRetrieveSerializer
        else:
            return serializers.FactorySerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return models.Factory.objects.all()

        else:
            factories = models.Employee.objects.filter(user=self.request.user, is_admin=True).values_list("factory")
            return models.Factory.objects.filter(id__in = factories)



# class AddEmployeeAPIView(generics.CreateAPIView):
#     serializer_class =