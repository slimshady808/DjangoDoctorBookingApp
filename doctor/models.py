from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
class DoctorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        doctor = self.model(email=email, **extra_fields)
        doctor.set_password(password)
        doctor.save(using=self._db)
        return doctor

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)








class Address(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.building}, {self.street}, {self.district}, {self.state}"


class Department(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='department_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Qualification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Slot(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    time = models.CharField(max_length=8, choices=[("10 AM", "10 AM"), ("10:20AM", "10:20AM"),
                                                  ("11:40AM", "11:40 AM"), ("12:00 PM", "12:00 PM"),
                                                  ("12:20 PM", "12:20 PM"), ("2:40 PM", "2:40 PM"),
                                                  ("3 PM", "3 PM"), ("3:20 PM", "3:20 PM"),
                                                  ("3:40 PM", "3:40 PM"), ("4:00 PM", "4:00 PM")])
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}-{self.doctor} - {self.date} {self.time} (Available: {self.is_available})"
    class Meta:
        unique_together = ['doctor', 'date', 'time']


class Doctor(AbstractBaseUser, PermissionsMixin):
    doctor_name = models.CharField(max_length=100)
    doctor_image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    doctor_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    fee = models.PositiveIntegerField()
    more_details= models.CharField(max_length=1000, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='doctor_users'  # Use a unique related_name for Doctor model
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='doctor_users'  # Use a unique related_name for Doctor model
    )

    objects = DoctorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['doctor_name']
    

    def __str__(self):
        return self.doctor_name
    
    def get_available_dates(self):
        tomorrow = timezone.now().date() + timedelta(days=1)
        six_days_later = timezone.now().date() + timedelta(days=6)

        available_dates = Slot.objects.filter(
            doctor=self,
            date__range=[tomorrow, six_days_later],
            is_available=True
        ).values_list('date', flat=True).distinct()

        return list(available_dates)

    def get_available_slots(self):
        return Slot.objects.filter(doctor=self, date__gte=timezone.now().date(), is_available=True)

    # def get_available_dates(self):
    #     available_dates = Slot.objects.filter(doctor=self, date__gte=timezone.now().date(),
    #                                           is_available=True).values_list('date', flat=True).distinct()
    #     return list(available_dates)
    def get_available_slots_by_date(self, selected_date):
        slots = Slot.objects.filter(doctor=self, date=selected_date, is_available=True)
        return slots

    def mark_date_unavailable(self, date):
        slots_to_mark_unavailable = Slot.objects.filter(doctor=self, date=date, is_available=True)
        for slot in slots_to_mark_unavailable:
            slot.is_available = False
            slot.save()

    def get_slot_choices(self, selected_date):
        available_slots = Slot.objects.filter(doctor=self, date=selected_date, is_available=True)
        choices = [(slot.time, slot.time) for slot in available_slots]
        return choices
