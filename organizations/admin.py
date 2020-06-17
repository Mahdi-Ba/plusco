from django.contrib import admin

# Register your models here.
from organizations.models import *


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    search_fields = ['title']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
        return False

    def has_delete_permission(self, request,obj=None):
        return False





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
    readonly_fields = ['user', 'owner']
    list_filter = ['status']
    autocomplete_fields = ['working_area', 'size']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'order','opposite_title']
    search_fields = ['title','opposite_title']


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['user', 'owner', 'source', 'target', 'type','status']
    search_fields = ['user', ]




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','factory' ]
    search_fields = ['title']

class CategoryModel(admin.TabularInline):
    model = Category
    extra = 1


class PartModel(admin.TabularInline):
    model = Part
    extra = 1


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    inlines = [PartModel]
    list_display = ['title', 'factory']
    search_fields = ['title']

class AreaModel(admin.TabularInline):
    model = Area
    extra = 1



@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['title','area' ]
    search_fields = ['title']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']



class RelModel(admin.TabularInline):
    model = Relation
    readonly_fields = ('user', 'owner')
    autocomplete_fields = ['source', 'target', 'type']
    fk_name = 'source'
    extra = 1


class DpartModel(admin.TabularInline):
    readonly_fields = ('user', 'owner')
    autocomplete_fields = ['status', ]
    model = Department
    extra = 1


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    inlines = (RelModel, DpartModel,CategoryModel,AreaModel)

    list_display = ['title', 'organization', 'en_title', 'owner', 'size', 'sort', 'status', 'user', 'updated_at']
    search_fields = ['title', 'en_title']
    readonly_fields = ['user', 'owner']
    list_filter = ['status']
    autocomplete_fields = ['working_area', 'size']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        for f in formset.forms:
            obj = f.instance
            obj.user = request.user
        super().save_formset(request, form, formset, change)


class AuthorityModel(admin.TabularInline):
    autocomplete_fields = ['user', 'department', 'status','position']
    model = UserAuthority
    extra = 1

class PositionModel(admin.TabularInline):
    list_display = ['title']
    model = Position
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = (AuthorityModel,PositionModel)

    list_display = ['title', 'user', 'status', 'factory']
    search_fields = ['title', ]
    readonly_fields = ['user', ]
    list_filter = ['status']
    autocomplete_fields = ['factory', 'status']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(UserAuthority)
class UserAuthorityAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'status']
    search_fields = ['user', ]
    # readonly_fields = ['user','department']
    list_filter = ['status']
    autocomplete_fields = ['user', 'department', 'status']


class AdminUserModel(admin.TabularInline):
    autocomplete_fields = ['user', 'status']
    model = AdminUser
    extra = 1


@admin.register(AdminGroup)
class AdminGroupAdmin(admin.ModelAdmin):
    inlines = (AdminUserModel,)
    list_display = ['owner', 'factory', 'user', 'status']
    search_fields = ['owner', ]
    list_filter = ['status',]
    autocomplete_fields = ['owner', 'factory', 'status']

    # def organization(self, obj):
    #     return obj.factory.organization.title




@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['admin_group', 'user', 'status']
    search_fields = ['user',]
    list_filter = ['status', 'admin_group']
    autocomplete_fields = ['user', 'admin_group', 'status']

