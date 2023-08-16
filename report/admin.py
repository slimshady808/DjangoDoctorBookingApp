from django.contrib import admin
from .models import TestTitle, Report, Test

@admin.register(TestTitle)
class TestTitleAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'description')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('symptoms', 'extra_notes', 'booking_id', 'doctor_id', 'patient_id')
    list_filter = ('booking_id', 'doctor_id', 'patient_id')
    search_fields = ('symptoms', 'booking_id__patient__user__username')  # Adjust search fields based on your models

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_title', 'report', 'date_of_test', 'result', 'notes')
    list_filter = ('test_title', 'date_of_test')
    search_fields = ('test_title__test_name', 'report__symptoms', 'report__booking_id__patient__user__username')  # Adjust search fields based on your models

