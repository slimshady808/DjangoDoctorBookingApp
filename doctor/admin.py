from django.contrib import admin
from .models import Address, Department, Qualification, Slot, Doctor

class AddressAdmin(admin.ModelAdmin):
    list_display = ('state', 'district', 'street', 'building')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

class QualificationAdmin(admin.ModelAdmin):
    list_display = ('title',)

class SlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'time', 'is_available')
    list_filter = ('doctor', 'date', 'is_available')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'doctor_department', 'phone', 'is_active', 'is_staff')
    list_filter = ('doctor_department', 'is_active', 'is_staff')
    search_fields = ('doctor_name', 'doctor_department__name', 'phone')
    ordering = ('doctor_name',)
    fieldsets = (
        (None, {'fields': ('user_profile', 'doctor_name', 'doctor_department', 'qualification')}),
        ('Contact Info', {'fields': ('phone', 'fee', 'address')}),
        ('Additional Info', {'fields': ('more_details',)}),
         ('Image', {'fields': ('doctor_image',)}),  
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

admin.site.register(Address, AddressAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Doctor,
                    #  DoctorAdmin
                     )

