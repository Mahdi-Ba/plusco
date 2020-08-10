from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    search_fields = ['title']


@admin.register(ActionStatus)
class ActionStatusAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    search_fields = ['title']



class ConformityGalleryModel(admin.TabularInline):
    model = ConformityGallery
    extra = 1

class ActionGalleryModel(admin.TabularInline):
    model = ActionGallery
    extra = 1
class ActionModel(admin.TabularInline):
    model = Action
    extra = 1

@admin.register(Conformity)
class ConformityAdmin(admin.ModelAdmin):
    inlines = [ConformityGalleryModel,ActionModel]

    list_display = [
        'text',
        'owner',
        'owner_factory',
        'receiver_factory',
        'part',
    ]
    search_fields = ['owner']
    list_filter = ['priority', 'is_conformity']
    autocomplete_fields = ['owner',
                           'owner_factory',
                           'receiver_factory',
                           'part',
                           'status'
                           ]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    inlines = [ActionGalleryModel]
    list_display = [
        'title',
        'conformity',
        'owner',
        'owner_factory',
        # 'followe_status',
        # 'follower_department',
        # 'executiv_status',
        'execute_department',
        'due_date',

    ]
    search_fields = ['title']

    autocomplete_fields = ['owner',
                           'conformity',
                           'owner_factory',
                           # 'follower_department',
                           'execute_department',
                           # 'followe_status',
                           # 'executiv_status',
                           'execute_owner',
                           # 'follower_owner',

                           ]


@admin.register(ConformityGallery)
class ConformityGalleryAdmin(admin.ModelAdmin):
    list_display = ['conformity', 'file']


@admin.register(ActionGallery)
class ActionGalleryAdmin(admin.ModelAdmin):
    list_display = ['action', 'file']
