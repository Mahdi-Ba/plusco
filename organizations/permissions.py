from rest_framework.permissions import BasePermission

from . import models


class CanEditOrganization(BasePermission):

    def has_object_permission(self, request, view, obj):
        obj: models.Organization
        if request.method == "GET":
            return True
        if obj.creator == request.user:
            return True
        else:
            return False
