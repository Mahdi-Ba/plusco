from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from datetime import timedelta, datetime


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, mobile, **extra_fields):
        """Create and save a User with the given mobile and password."""

        if not mobile:
            raise ValueError('The given mobile must be set')

        user = self.model(mobile=mobile, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, **extra_fields):

        """Create and save a regular User with the given mobile and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, **extra_fields)

    def create_superuser(self, mobile, **extra_fields):
        """Create and save a SuperUser with the given mobile and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = None
    password = None
    mobile = models.CharField(max_length=32, unique=True)
    national_code = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_complete_registered(self):
        if self.first_name is None or self.last_name is None:  # PROPOSED also national code
            return False
        if len(self.first_name) == 0 or len(self.last_name) == 0:
            return False
        return True


class OTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\d+$', message="لطفا مقدار معتبر وارد کنید")
    # database field
    mobile = models.CharField(max_length=10, validators=[phone_regex])
    otp = models.CharField(max_length=300)  # One Time Password
    create_time = models.DateTimeField(auto_now_add=True)  # time that save in database
    duration = models.DurationField(default=timedelta(minutes=2))  # duration for expired

    @property
    def expired(self):
        """
        return a boolean
        if OTP(one time password) is expired return True
        if not expired return False
        """
        if self.create_time.replace(
                tzinfo=None) + self.duration < datetime.utcnow():
            return True
        else:
            return False
