from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from organizations.models import Factory, Category, Department, Part
from users.models import User


class Status(models.Model):
    title = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=None)

    def __str__(self):
        return self.title


class Conformity(models.Model):
    # is_publish = models.BooleanField(default=True)
    # publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='publisher')
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    owner_factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True, blank=True,related_name='owner_factory')
    receiver_factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, blank=True)
    is_conformity = models.BooleanField(default=False)


    def __str__(self):
        return self.text



class ConformityGallery(models.Model):
    conformity = models.ForeignKey(Conformity, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='conformity/', null=True, blank=True)



class ActionStatus(models.Model):
    title = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=None)

    def __str__(self):
        return self.title

class Action(models.Model):
    # is_publish = models.BooleanField(default=True)
    # publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    followe_status = models.ForeignKey(ActionStatus, on_delete=models.SET_NULL, null=True, blank=True,related_name='follower_status')
    follower_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,related_name='follower_dep')
    execute_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='execute_owner')
    executiv_status = models.ForeignKey(ActionStatus, on_delete=models.SET_NULL, null=True, blank=True,related_name='executive_status')
    execute_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,related_name='execute_dep')
    follower_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='follower_owner')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='action_owner')
    owner_factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True, blank=True)
    conformity = models.ForeignKey(Conformity, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.title

class ActionGallery(models.Model):
    action = models.ForeignKey(Action, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='action/', null=True, blank=True)


