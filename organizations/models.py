from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from users.models import User

class Status(models.Model):
    title = models.CharField(max_length=255,unique=True)
    order = models.IntegerField(default=None)

    def __str__(self):
        return self.title

class WorkingArea(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    en_title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    text = RichTextUploadingField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    sort = models.IntegerField(null=True, blank=True)
    image_alt = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='working_area/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class OrganizationSize(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    en_title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    sort = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Organization(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owner')
    size = models.ForeignKey(OrganizationSize, on_delete=models.SET_NULL, null=True, blank=True)
    working_area = models.ManyToManyField(WorkingArea, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    en_title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    image = models.ImageField(upload_to='company/', null=True, blank=True)
    image_alt = models.CharField(max_length=255, null=True, blank=True)
    text = RichTextUploadingField(blank=True, null=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    index = models.BooleanField(default=False)
    sort = models.BigIntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Factory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='factoryowner')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True,related_name='userresume')
    size = models.ForeignKey(OrganizationSize, on_delete=models.SET_NULL, null=True, blank=True)
    working_area = models.ManyToManyField(WorkingArea, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    en_title = models.CharField(max_length=255, null=True, blank=True,unique=True)
    image = models.ImageField(upload_to='company/', null=True, blank=True)
    image_alt = models.CharField(max_length=255, null=True, blank=True)
    text = RichTextUploadingField(blank=True, null=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    index = models.BooleanField(default=False)
    trusted = models.BooleanField(default=False)
    master = models.BooleanField(default=False)
    sort = models.BigIntegerField(null=True, blank=True)
    relation = models.ManyToManyField('self', through='Relation',through_fields=('source','target'), symmetrical=False)

    class Meta:
        unique_together = ('organization', 'title',)



    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title + "("+ self.organization.title + ")"

class RelationType(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    order = models.IntegerField()

    def __str__(self):
        return self.title

class Relation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='relowner')
    source = models.ForeignKey(Factory,related_name='source',on_delete=models.SET_NULL,null=True)
    target = models.ForeignKey(Factory,related_name='target',on_delete=models.SET_NULL,null=True)
    type = models.ForeignKey(RelationType,on_delete=models.SET_NULL,null=True)


class Department(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='depowner')
    title = models.CharField(max_length=255,blank=True,null=True)
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.title)

class Category(models.Model):
    title = models.CharField(max_length=255,unique=True)
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.title)

class Area(models.Model):
    title = models.CharField(max_length=255, unique=True)
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.title)

class Part(models.Model):
    title = models.CharField(max_length=255, unique=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.title)

class Position(models.Model):
    title = models.CharField(max_length=255, unique=True)


class UserAuthority(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user.mobile)


class AdminGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='adminowner')
    factory = models.OneToOneField(Factory, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.factory)



class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_group = models.ForeignKey(AdminGroup, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user.mobile)


