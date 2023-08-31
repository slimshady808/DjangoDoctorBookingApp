from django.db import models
from doctor.models import Slot,Doctor
from account.models import Patient
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancel', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('online', 'Online Payment'),
        ('wallet', 'Wallet'),
    ]

    booking_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES,default='online')
    token = models.CharField(max_length=6, unique=True, editable=False)
    

    def save(self, *args, **kwargs):
        if not self.token:
            # Generate a unique 6-digit token using a combination of random digits
            self.token = str(uuid.uuid4().int)[:6]
        super(Booking, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking ID: {self.booking_id}, Patient: {self.patient_id}, Doctor: {self.doctor}, Date: {self.date_of_booking}, Slot: {self.slot}, Status: {self.get_status_display()}, Payment Type: {self.get_payment_type_display()}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    isPaid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)
        if self.booking and self.isPaid:
            self.booking.slot.is_available = False
            self.booking.slot.save()

    def __str__(self):
        return f"Payment for Booking {self.booking.booking_id} "    