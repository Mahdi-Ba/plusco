from django.db import models
from users.models import User


class User(User):
    class Meta:
        proxy = True


class Message(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True, max_length=200, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True, null=True)
    # sender = models.ForeignKey(User, null=True, blank=True)
