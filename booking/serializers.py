from rest_framework import serializers
from .models import Booking,Payment

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Payment
        fields='__all__'
        depth= 2


