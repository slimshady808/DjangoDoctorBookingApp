from rest_framework import serializers
from .models import UserProfile, Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    patient_profile = PatientSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id','username', 'email', 'user_type', 'is_active', 'is_staff', 'image_of_user', 'patient_profile')
        read_only_fields = ('id', 'is_staff')

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)