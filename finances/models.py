from django.db import models

from organizations.models import Factory
from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class Plan(models.Model):
    price = models.DecimalField(max_digits=15, decimal_places=0)
    percent = models.FloatField()
    price_with_tax = models.DecimalField(max_digits=15, decimal_places=0)
    count = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    month = models.IntegerField()
    is_free = models.BooleanField(default=False)


class FactoryPlan(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    count = models.IntegerField()
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    price = models.DecimalField(max_digits=15, decimal_places=0)
    percent = models.FloatField()
    price_with_tax = models.DecimalField(max_digits=15, decimal_places=0)
    is_success = models.BooleanField(default=False)

