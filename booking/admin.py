from django.contrib import admin
from .models import Booking,Payment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'patient_id', 'doctor', 'date_of_booking', 'status', 'payment_type')
    list_filter = ('doctor', 'status', 'payment_type')
    search_fields = ('booking_id', 'patient_id__username', 'doctor__name', 'date_of_booking')
    ordering = ('-date_of_booking',)

from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'payment_id', 'amount', 'isPaid', 'payment_date')
    list_filter = ('isPaid',)
    search_fields = ('booking__booking_id', 'payment_id')
    readonly_fields = ('payment_date',)

admin.site.register(Payment, PaymentAdmin)
