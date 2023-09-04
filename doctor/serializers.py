from rest_framework import serializers
from .models import Address, Department, Qualification, Slot, Doctor
from account.models import UserProfile
from account.serializers import UserProfileSerializer
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
    #user_profile_id = serializers.PrimaryKeyRelatedField(source='user_profile', read_only=True)
    class Meta:
        model = Doctor
        #fields = ('id','doctor_image', 'doctor_name', 'doctor_department', 'qualification', 'phone', 'fee', 'more_details', 'address', 'is_active', 'is_staff', 'user_profile_id')
        fields='__all__'


# class DoctorSerializer(serializers.ModelSerializer):
#     available_dates = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Doctor
#         fields = (
#             'id', 'doctor_name', 'doctor_department', 'qualification', 'phone', 'fee', 'more_details',
#             'address', 'is_active', 'is_staff', 'available_dates', 'available_slots'
#         )
#         read_only_fields = ('id', 'is_active', 'is_staff')

#     def get_available_dates(self, obj):
#         return obj.get_available_dates()

#     def get_available_slots(self, obj):
#         return obj.get_available_slots()


# serializers.py

from rest_framework import serializers
from .models import Doctor

class DoctorRegistrationSerializer(serializers.Serializer):
    doctor_name = serializers.CharField(max_length=100)
    doctor_image = serializers.ImageField(required=False)
    doctor_department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    qualification = serializers.PrimaryKeyRelatedField(queryset=Qualification.objects.all())
    phone = serializers.CharField(max_length=15)
    fee = serializers.IntegerField()
    more_details = serializers.CharField(max_length=1000, required=False)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        if 'doctor_image' not in validated_data:
            validated_data['doctor_image'] = None
        user_profile = UserProfile.objects.create_user(
            email=validated_data['email'],
            user_type='doctor',
            password=validated_data['password'],
            username=validated_data['username']
        )

        doctor = Doctor.objects.create(
            user_profile=user_profile,
            doctor_name=validated_data['doctor_name'],
            doctor_image=validated_data.get('doctor_image'),
            doctor_department=validated_data['doctor_department'],
            qualification=validated_data['qualification'],
            phone=validated_data['phone'],
            fee=validated_data['fee'],
            more_details=validated_data.get('more_details'),
            address=validated_data['address']
        )

        return doctor

