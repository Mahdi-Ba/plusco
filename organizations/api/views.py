from rest_framework import views, generics, permissions as django_permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from .. import models, permissions


# from rest_framework.filters import SearchFilter, OrderingFilter


class OrganizationListAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()


class OrganizationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsCompleteRegistry,
                          permissions.CanEditOrganization]
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return models.Organization.objects.all()

        else:
            return models.Organization.objects.filter(creator=self.request.user)


class FactoryCreateByExistedOrganization(generics.CreateAPIView):
    permission_classes = [permissions.IsCompleteRegistry]
    serializer_class = serializers.CreateNewFactoryByExistedOrganization

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FactoryCreateByNotExistedOrganization(generics.CreateAPIView):
    permission_classes = [permissions.IsCompleteRegistry]
    serializer_class = serializers.CreateNewFactoryByNotExistedOrganization

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FactoryListAPIView(generics.ListAPIView):
    permission_classes = [django_permissions.AllowAny]
    serializer_class = serializers.FactorySerializer
    queryset = models.Factory.objects.all()


class FactoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsCompleteRegistry]

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
            return models.Factory.objects.filter(id__in=factories)


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.AddEmployeeSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = ["job_title", "is_admin", "use_license", "status"]

    def get_permissions(self):
        permission_classes = [permissions.IsCompleteRegistry]

        if self.request.method != "GET":
            permission_classes.append(permissions.IsFactoryAdmin)

        return super(EmployeeListCreateAPIView, self).get_permissions()

    def get_factory(self):
        pk = self.kwargs["factory_pk"]
        try:
            factory = models.Factory.objects.get(pk=pk)
            return factory
        except Exception:
            return None

    def get_queryset(self):
        factory = self.get_factory()
        return models.Employee.objects.filter(factory=factory)

    def perform_create(self, serializer):
        factory = self.get_factory()
        serializer.save(factory=factory)
