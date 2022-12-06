import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        print(f"PASSWORD : {password}")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.us_admin = True
        user.save(using=self._db)
        return user


class UserData(AbstractUser, PermissionsMixin):
    id           = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(unique=True)
    is_active    = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_admin     = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['email']


class Profile(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user          = models.OneToOneField(UserData, on_delete=models.CASCADE)
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    picture       = models.ImageField(default='default_user.jpg', upload_to='profile_pics')
    bio           = models.TextField(blank=True, null=True)


class Author(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user          = models.OneToOneField(UserData, on_delete=models.CASCADE)
    pen_name      = models.CharField(max_length=100)
    picture       = models.ImageField(default='default_user.jpg', upload_to='profile_pics')
    bio           = models.TextField(blank=True, null=True)
