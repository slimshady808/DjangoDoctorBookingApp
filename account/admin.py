from django.contrib import admin
from .models import User, Patient

# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'is_active', 'is_admin', 'is_staff']
    search_fields = ['email', 'username']
    list_filter = ['is_active', 'is_admin', 'is_staff']
    # Add any other customization you need for the User admin page

# Register the Patient model
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'mobile_number', 'place', 'age']
    search_fields = ['name', 'mobile_number', 'place']
    list_filter = ['user', 'place']
    # Add any other customization you need for the Patient admin page

