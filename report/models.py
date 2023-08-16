from django.db import models
from account.models import Patient
from booking.models import Booking
from doctor.models import Doctor

class TestTitle(models.Model):
    test_name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.test_name

class Report(models.Model):
    symptoms = models.CharField(max_length=255)
    extra_notes = models.TextField(blank=True)
    medicine=models.CharField(max_length=255)
    booking_id=models.ForeignKey(Booking,on_delete=models.CASCADE)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)

    def __str__(self):
        return f"Report ID: {self.pk}"
    def save(self, *args, **kwargs):
        # Update the booking status to "completed" when the report is saved
        self.booking_id.status = 'completed'
        self.booking_id.save()
        super().save(*args, **kwargs)

class Test(models.Model):
    test_title = models.ForeignKey(TestTitle, on_delete=models.CASCADE, related_name='tests')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='tests')
    date_of_test = models.DateField()
    result = models.FileField(upload_to='test_results/',blank=True)
    notes=models.CharField(max_length=255)

    def __str__(self):
        return f"Test ID: {self.pk} - {self.test_title}"









# from django.db import models

# # Create your models here.
# class TestTitle(models.Model):
#     test_name=models.CharField(max_length=30)
#     description=models.TextField(blank=True)

#     def __str__(self) :
#         return self.test_name
    
# class Report(models.Model):
#     symptoms=models.CharField(max_length=255)
#     extra_notes=models.TextField(blank=True)

#     def __str__(self):
#         return f"Report ID: {self.report_id}"

# class Test(models.Model):
#     test_title= models.ForeignKey(TestTitle,on_delete=models.CASCADE)
#     report=models.ForeignKey(Report,on_delete=models.CASCADE)
#     date_of_test=models.DateField()
#     result=models.CharField(max_length=255)

# class Medicine(models.Model):
#     medicine_name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.medicine_name

# class ReportMedicine(models.Model):
#     report=models.ForeignKey(Report,on_delete=models.CASCADE)
#     medicine=models.ForeignKey(Medicine,on_delete=models.CASCADE)

        