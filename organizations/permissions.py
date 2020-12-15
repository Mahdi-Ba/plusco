from rest_framework.permissions import BasePermission

from . import models


class IsCompleteRegistry(BasePermission):
    message = "نیازمند ورود یا تکمیل اطلاعات هستید"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_complete_registered)


class CanEditOrganization(BasePermission):
    message = "شما اجازه‌ی ویرایش سازمان را ندارید"

    def has_object_permission(self, request, view, obj):
        obj: models.Organization
        if request.method == "GET":
            return True
        if obj.creator == request.user:
            return True
        else:
            return False


class IsFactoryAdmin(BasePermission):
    message = "شما مدیر این کارگاه نیستید"

    def has_permission(self, request, view):
        try:
            factory = view.get_factory()
            qs = models.Employee.objects.filter(factory=factory, is_admin=True, user=request.user, status="a")
            if qs.exists():
                return True
            else:
                return False
        except Exception as e:
            return False
