# from django.contrib import admin

# # Register your models here.
from organizations import models
from django.contrib import admin

admin.site.register(models.Organization)
admin.site.register(models.Factory)
admin.site.register(models.Group)
admin.site.register(models.Employee)
admin.site.register(models.JobTitle)


