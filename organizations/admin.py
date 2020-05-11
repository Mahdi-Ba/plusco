from django.contrib import admin

# Register your models here.
from organizations.models import *


@admin.register(WorkingArea)
class WorkingAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'en_title', 'user', 'sort', 'status', 'updated_at']
    search_fields = ['title', 'en_title']
    readonly_fields = ['user']
    list_filter = ['status']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

#
@admin.register(OrganizationSize)
class OrganizationSizeAdmin(admin.ModelAdmin):
    list_display = ['title', 'en_title', 'user', 'sort', 'status', 'updated_at']
    search_fields = ['title', 'en_title']
    readonly_fields = ['user']
    list_filter = ['status']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)



@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['title', 'en_title', 'owner', 'size', 'sort', 'status', 'user', 'updated_at']
    search_fields = ['title', 'en_title']
    readonly_fields = ['user','owner']
    list_filter = ['status']
    autocomplete_fields = ['working_area','size']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ['title','user','order']
    search_fields = ['title']


@admin.register(Relation)
class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ['user','owner','source','target','type']
    search_fields = ['user',]

class relModel(admin.TabularInline):
    model = Relation
    readonly_fields = ('user', 'owner')
    autocomplete_fields = ['source','target','type']
    fk_name = 'source'
    extra = 1



@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    inlines = (relModel,)

    list_display = ['title', 'en_title', 'owner', 'size', 'sort', 'status', 'user', 'updated_at']
    search_fields = ['title', 'en_title']
    readonly_fields = ['user','owner']
    list_filter = ['status']
    autocomplete_fields = ['working_area','size']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        for f in formset.forms:
            obj = f.instance
            obj.user = request.user
        super().save_formset(request, form, formset, change)

