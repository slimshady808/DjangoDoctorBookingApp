from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import  login
from .models import Doctor,Department,Address,Slot
from .serializers import DoctorSerializer,DepartmentSerializer,AddressSerializer,QualificationSerializer,SlotSerializer,DoctorRegistrationSerializer
from account.serializers import UserProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from .models import Department, Qualification
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone
from django.db import transaction
from account.models import UserProfile
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh'
    ]
    return Response(routes)

# class DoctorRegistrationView(APIView):
#     def post(self,request):
#         print(request.data,'datas')
#         serializer=DoctorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # Hash the password before saving the doctor
#         password= request.data['password']
#         hashed_password=make_password(password)
#         serializer.save(password=hashed_password)
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

class Departments(APIView):
    def get (self,request):
        departments=Department.objects.all()

        serializer = DepartmentSerializer(departments,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK )
class Qualifications(APIView):
    def get (self,request):
        qualifications=Qualification.objects.all()

        serializer =QualificationSerializer(qualifications,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)   
    


# class DoctorList(APIView):
#     def get(self, request):
#         doctors = UserProfile.objects.filter(user_type='doctor')
#         serializer = UserProfileSerializer(doctors, many=True)  # Use UserProfileSerializer
#         data = serializer.data

#         for doctor in data:
#             # Access additional details using doctor['field_name']
#             department_id = doctor['doctor_profile']['doctor_department']
#             department = Department.objects.get(id=department_id)
#             doctor['department_name'] = department.name

#         return Response(data, status=status.HTTP_200_OK)
    
class DoctorList(APIView):
    def get(self,request):
        print('hii')
        doctors=Doctor.objects.all()
        serializer=DoctorSerializer(doctors,many=True)
        data=serializer.data

        for doctor in data:
            department_id=doctor['doctor_department']
            department=Department.objects.get(id=department_id)
            doctor['department_name']=department.name
        
        return Response (serializer.data,status=status.HTTP_200_OK)



# class DoctorRegisterationView(APIView):
#     def post(self,request):
      
#         doctor_data={
#             "doctor_name": request.data.get("doctor_name"),
#             "doctor_image":request.data.get("doctor_image"),
#             "doctor_department": request.data.get("doctor_department"),
#             "qualification": request.data.get("qualification"),
#             "phone": request.data.get("phone"),
#             "fee": request.data.get("fee"),
#             "more_details": request.data.get("more_details"),
#             "address": request.data.get("address"),
#         }

#         user_data={
#             "username": request.data.get("username"),
#             "email":request.data.get("email"),
#             "password":make_password(request.data.get("password")),
#             "user_type":"doctor",
#         }

#         with transaction.atomic():
#             #create the UserProfile instance first
#             user_serializer=UserProfileSerializer(data=user_data)
#             user_serializer.is_valid(raise_exception=True)
#             user_instance=user_serializer.save()
            
#             #Associate the user_profile instance with doctor_data
#             doctor_data["user_profile"]=user_instance.id

#             #create the Doctor Instance

#             doctor_serializer=DoctorSerializer(data=doctor_data)
            
#             doctor_serializer.is_valid(raise_exception=True)

#             doctor_instance=doctor_serializer.save()
        
#         return Response(
#             {"user_profile":user_serializer.data,"doctor":doctor_serializer.data},
#             status=status.HTTP_201_CREATED
#         )
    
# class DoctorRegisterationView(APIView):
#     def post(self, request):
#         doctor_data = {
#             "doctor_name": request.data.get("doctor_name"),
#             "doctor_image": request.data.get("doctor_image"),
#             "doctor_department": request.data.get("doctor_department"),
#             "qualification": request.data.get("qualification"),
#             "phone": request.data.get("phone"),
#             "fee": request.data.get("fee"),
#             "more_details": request.data.get("more_details"),
#             "address": request.data.get("address"),
            
#         }

#         user_data = {
#             "username": request.data.get("username"),
#             "email": request.data.get("email"),
#             "password": make_password(request.data.get("password")),
#             "user_type": "doctor",
#         }

#         with transaction.atomic():
#             # Create the UserProfile instance first
#             user_serializer = UserProfileSerializer(data=user_data)
#             user_serializer.is_valid(raise_exception=True)
#             user_instance = user_serializer.save()

#             # Associate the user_profile instance with doctor_data
#             print('user instance',user_instance.id)
#             # doctor_data["user_profile"] = user_instance.id

#             # Create the Doctor Instance
#             doctor_serializer = DoctorSerializer(data=doctor_data)
#             doctor_serializer.is_valid(raise_exception=True)
#             doctor_instance = doctor_serializer.save()

#         return Response(
#             {"user_profile": user_serializer.data, "doctor": doctor_serializer.data},
#             status=status.HTTP_201_CREATED
#         )

@api_view(['POST'])
def register_doctor(request):
    if request.method == 'POST':
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Extract data from the serializer
                    email = serializer.validated_data['email']
                    password = serializer.validated_data['password']
                    doctor_name = serializer.validated_data['doctor_name']
                    doctor_image = serializer.validated_data['doctor_image']
                    doctor_department = serializer.validated_data['doctor_department']
                    qualification = serializer.validated_data['qualification']
                    phone = serializer.validated_data['phone']
                    fee = serializer.validated_data['fee']
                    more_details = serializer.validated_data['more_details']
                    address = serializer.validated_data['address']
                    username = serializer.validated_data['username']
                    
                    # Create a user profile with user_type 'doctor'
                    user_profile = UserProfile.objects.create_user(
                        email=email,
                        user_type='doctor',
                        password=password,
                        username=username
                    )
                    
                    # Create the doctor using the associated user profile
                    doctor = Doctor.objects.create(
                        user_profile=user_profile,
                        doctor_name=doctor_name,
                        doctor_image=doctor_image,
                        doctor_department=doctor_department,
                        qualification=qualification,
                        phone=phone,
                        fee=fee,
                        more_details=more_details,
                        address=address
                    )
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_doctors_by_department(request,department_id):
    try:
        doctors=Doctor.objects.filter(doctor_department=department_id)
        serializer=DoctorSerializer(doctors,many=True)
        data=serializer.data

        department=Department.objects.get(id=department_id)
        department_name=department.name
        for doctor in data:
            doctor['department_name']=department_name
        return Response(data, status=status.HTTP_200_OK) 
    except Doctor.DoesNotExist:
        return Response({'detail': "Department not found"}, status=status.HTTP_404_NOT_FOUND)
    

class DoctorListView(ListAPIView):
    serializer_class=DoctorSerializer
    filter_backends=[filters.SearchFilter,filters.OrderingFilter]
    search_fields=['doctor_name']
    ordering_fields=['fee']

    def get_queryset(self):
        queryset=Doctor.objects.all()
        department_id=self.request.query_params.get('department_id')
        if department_id:
            queryset=queryset.filter(doctor_department_id=department_id)
        return queryset
    
class DoctorDetailView(RetrieveUpdateAPIView):
    queryset=Doctor.objects.all()
    serializer_class=DoctorSerializer

class AddressDetailView(RetrieveUpdateAPIView):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer


class AddressCreateView(APIView):
    def post(self,request):
        print(request.data,'new')
        serializer=AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])  
def department_byId(request,department_id):
    try:
        department=Department.objects.get(id=department_id)
        serializer=DepartmentSerializer(department)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Department.DoesNotExist:
        return Response({'detail':"Department not found"},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def qualification_ById(request,qualification_id):
    try:
        qualification=Qualification.objects.get(id=qualification_id)
        serializer=QualificationSerializer(qualification)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Qualification.DoesNotExist:
        return Response({'detail':"qualification not found"},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_available_dates(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        available_dates = doctor.get_available_dates()
        return Response({'available_dates': available_dates}, status=status.HTTP_200_OK)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_available_slots(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

    selected_date = request.query_params.get('date')
    if not selected_date:
        return Response({'error': 'Date parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        slots = doctor.get_available_slots_by_date(selected_date)
        serializer = SlotSerializer(slots, many=True)
        return Response({'available_slots': serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        print("Exception:", e) 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_date_and_time(request, slotId):
    try:
        slot = Slot.objects.get(id=slotId)
        serializer = SlotSerializer(slot)

        # Retrieve the doctor_name from the related Doctor object
        doctor_name = slot.doctor.doctor_name
       
        # Add doctor_name to the serializer data
        serializer.data['doctor_name'] = doctor_name

       
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Slot.DoesNotExist:
        return Response({'error': 'slot does not exist'}, status=status.HTTP_404_NOT_FOUND)