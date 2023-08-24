# chat/serializers.py

from rest_framework import serializers
from .models import UserToDoctorMessage, DoctorToUserMessage

class UserToDoctorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToDoctorMessage
        fields = '__all__'

class DoctorToUserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorToUserMessage
        fields = '__all__'
