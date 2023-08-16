from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField(source='doctor.doctor_name')
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'content', 'rating', 'created_at', 'doctor_name', 'user_name','user','doctor']
