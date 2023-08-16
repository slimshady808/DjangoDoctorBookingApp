from rest_framework import serializers
from .models import Address, Department, Qualification, Slot, Doctor

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class SlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField(source='doctor.doctor_name')
    class Meta:
        model = Slot
        fields = ['id', 'time', 'date', 'is_available', 'doctor', 'doctor_name']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
