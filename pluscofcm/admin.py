from django.contrib import admin
from fcm_django.models import FCMDevice
from fcm_django.admin import DeviceAdmin
from django.shortcuts import render
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect
from .models import User,Message
from plusco.settings import BASE_URL


# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'first_name', 'last_name')
    search_fields = ('mobile', 'first_name', 'last_name')
    ordering = ('mobile',)
    actions = ['gardeshMessage']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
        return False

    def has_delete_permission(self, request,obj=None):
        return False


    def gardeshMessage(self, request, queryset):

        if request.POST.get('apply', False):
            if request.POST.get('type') == 'all':
                deviceset = FCMDevice.objects.filter(user__in=queryset).all()
            else:
                deviceset = FCMDevice.objects.filter(user__in=queryset, type=request.POST.get('type')).all()
            deviceset.send_message(title=request.POST.get('title'), body=request.POST.get('message'))
            message_list = []
            for user in queryset:
                message_list.append(Message(title=request.POST['title'],message=request.POST['message'],type = request.POST['type'],user=user))
            Message.objects.bulk_create(message_list)
            # return HttpResponseRedirect(redirect_to='http://127.0.0.1:8080/admin/gpayfcm/user/')
            return HttpResponseRedirect(redirect_to=BASE_URL+'admin/pluscofcm/user/')

        else:
            form = queryset
            return render(request, 'fcm/index.html',
                          {'form': form, 'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, })


# @admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'date')
    search_fields = ('user__mobile',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

