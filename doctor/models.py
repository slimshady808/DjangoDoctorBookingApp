from django.db import models
from account.models import UserProfile
from django.utils import timezone
from datetime import timedelta
# Create your models here.
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

class Doctor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='doctor_profile')
    doctor_name = models.CharField(max_length=100)
    doctor_image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    doctor_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    fee = models.PositiveIntegerField()
    more_details = models.CharField(max_length=1000, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}-{self.doctor_name}"

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