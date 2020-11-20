from django.db import models

# Create your models here.
from organizations.models import Factory, Department
from users.models import User


class Status(models.Model):
    title = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=None)

    def __str__(self):
        return self.title


class Inspection(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    owner_factory = models.ForeignKey(Factory, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='inspection_owner_factory')
    receiver_factory = models.ForeignKey(Factory, on_delete=models.CASCADE, null=True, blank=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Conformity(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='conformity')
    receiver_department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    is_conformity = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True, )
    due_date = models.DateField(null=True, blank=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text


class ConformityGallery(models.Model):
    conformity = models.ForeignKey(Conformity, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='conformity_gallery')
    file = models.FileField(upload_to='conformity/', null=True, blank=True)


class ActionStatus(models.Model):
    title = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=None)

    def __str__(self):
        return self.title


class Action(models.Model):
    status = models.ForeignKey(ActionStatus, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='executive_status')
    execute_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='execute_owner')

    conformity = models.ForeignKey(Conformity, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='action')
    title = models.CharField(max_length=255, blank=True, null=True)
    reply_text = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class ActionGallery(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True, blank=True, related_name='action_gallery')
    file = models.FileField(upload_to='action/', null=True, blank=True)
