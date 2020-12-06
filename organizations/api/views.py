from rest_framework import views, generics, permissions
from rest_framework.response import Response
from . import serializers
from .. import models
from rest_framework import status


class OrganizationListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()


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
