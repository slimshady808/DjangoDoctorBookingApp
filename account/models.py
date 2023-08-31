from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
class UserProfileManager(BaseUserManager):
    def create_user(self, email, user_type, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_type, password=None):
        if user_type != 'admin':
            raise ValueError("Superuser must have user_type='admin'")
        return self.create_user(email, user_type, password=password, is_staff=True, is_superuser=True)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('user', 'User'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES,default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image_of_user = models.ImageField(upload_to='user_profile_images/', blank=True, null=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    objects = UserProfileManager()

  

    def __str__(self):
        return f"{self.email}-{self.id}"
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='user_profile_groups'  # Use a unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='user_profile_user_permissions'  # Use a unique related_name
    )
    
class Patient(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='patient_profile')
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    place = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    summary = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
