from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        """Create and save a User with the given mobile and password."""

        if not mobile:
            raise ValueError('The given mobile must be set')
        
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        
        """Create and save a regular User with the given mobile and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        """Create and save a SuperUser with the given mobile and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, password, **extra_fields)

class User(AbstractUser):
    """User model."""

    username = None
    mobile = models.CharField(db_index=True, max_length=32, unique=True)
    national_code = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    say_hi = models.BooleanField(default=False)
    expire_pass = models.BooleanField(default=True)
    file = models.FileField(upload_to='users/',blank=True, null=True)
    # attrs = JSONField(null=True, blank=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = UserManager()