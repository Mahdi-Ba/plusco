from django.db import models
from django_jalali.db import models as jalali_models


class Organization(models.Model):
    complete_name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="organization/",null=True)
    creator = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    create_at = jalali_models.jDateTimeField(auto_now_add=True)
    update_at = jalali_models.jDateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name


class Factory(models.Model):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    is_central_office = models.BooleanField(default=False)
    creator = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("organization", "name")

    @property
    def groups(self):
        employees = list(Employee.objects.filter(factory=self))
        groups = []
        for employee in employees:
            for group in list(Group.objects.filter(employees=employee)):
                if group not in groups:
                    groups.append(group)
        return groups


class JobTitle(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Employee(models.Model):
    factory = models.ForeignKey("Factory", on_delete=models.CASCADE, related_name="employees")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="employees")
    job_title = models.ForeignKey("JobTitle", on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    use_license = models.BooleanField(default=True)

    # TODO  add status  for employee (pending,reject,....)

    class Meta:
        unique_together = ("factory", "user")


class Group(models.Model):
    name = models.CharField(max_length=150)
    employees = models.ManyToManyField("Employee", related_name="groups")
    creator = models.ForeignKey("Employee", related_name="created_groups", on_delete=models.SET_NULL, null=True)

    @property
    def factory(self):
        if self.creator is not None:
            return self.creator.factory
        else:
            try:
                self.employees[0].factory
            except:
                return None
