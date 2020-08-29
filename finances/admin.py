from django.contrib import admin

# Register your models here.
from finances.models import Category, Plan, FactoryPlan


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'price',
        'percent',
        'price_with_tax',
        'count',
        'category',
        'month',
        'is_free',
    ]
    list_filter = ['category', 'is_free']


@admin.register(FactoryPlan)
class FactoryPlanAdmin(admin.ModelAdmin):
    list_display = [
        'factory',
        'user',
        'count',
        'start_date',
        'end_date',
        'price',
        'is_success'
    ]
    list_filter = ['is_success']
    search_fields = ['factory__title',]

