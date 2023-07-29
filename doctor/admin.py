from django.contrib import admin
from .models import Doctor, Address, Department, Qualification, Slot

# Customizing the Doctor Admin
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'email', 'doctor_department', 'qualification', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'doctor_department', 'qualification')
    search_fields = ('doctor_name', 'email', 'phone')
    ordering = ('doctor_name',)
    filter_horizontal = ('groups', 'user_permissions')

# Registering the models with their respective admins
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Address)
admin.site.register(Department)
admin.site.register(Qualification)
admin.site.register(Slot)

