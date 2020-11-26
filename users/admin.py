"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User


# from django_json_widget.widgets import JSONEditorWidget
# from jsonfield import JSONField

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no mobile field."""
    # formfield_overrides = {
    #     fields.JSONField: {'widget': JSONEditorWidget},a
    # }
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'national_code', 'birth_date', 'file', 'trusted')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2'),
        }),
    )
    list_display = ('mobile', 'first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('mobile', 'first_name', 'last_name', 'email')
    ordering = ('mobile',)
