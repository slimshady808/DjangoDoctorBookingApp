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
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

from account.models import UserProfile
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh'
    ]
    return Response(routes)



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
    


    
class DoctorList(APIView):
    def get(self,request):
        
        doctors=Doctor.objects.all()
        serializer=DoctorSerializer(doctors,many=True)
        data=serializer.data

        for doctor in data:
            department_id=doctor['doctor_department']
            department=Department.objects.get(id=department_id)
            user_id=doctor['user_profile']
            user=UserProfile.objects.get(id=user_id)
            doctor['department_name']=department.name
            doctor['email']=user.email
        
        return Response (serializer.data,status=status.HTTP_200_OK)




    
class DoctorRegisterationView(APIView):
    def post(self, request):
        print(request.data)
        doctor_data = {
            "doctor_name": request.data.get("doctor_name"),
            "doctor_image": request.data.get("doctor_image"),
            "doctor_department": request.data.get("doctor_department"),
            "qualification": request.data.get("qualification"),
            "phone": request.data.get("phone"),
            "fee": request.data.get("fee"),
            "more_details": request.data.get("more_details"),
            "address": request.data.get("address"),
            
        }

        user_data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
           
            # "password": request.data.get("password"),
            "user_type": "doctor",
        }

        with transaction.atomic():
           
            user_serializer = UserProfileSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            password=make_password('newpassword')
            user_serializer.save(password=password)
            user_instance = user_serializer.save()

            # Associate the user_profile instance with doctor_data
            print('user instance',user_instance.id)
            doctor_data["user_profile"] = user_instance.id
            print (doctor_data)
            # Create the Doctor Instance
            doctor_serializer = DoctorSerializer(data=doctor_data)
            doctor_serializer.is_valid(raise_exception=True)
            doctor_instance = doctor_serializer.save()

        return Response(
            {"user_profile": user_serializer.data, "doctor": doctor_serializer.data},
            status=status.HTTP_201_CREATED
        )


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
     
        serializer=AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SlotCreateView(APIView):
    def post(self,request):
    
        doc_id=request.data['doctor']
        try:
            user=UserProfile.objects.get(id=doc_id)
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found")
        try:
            doctor=Doctor.objects.get(user_profile=user)
        except Doctor.DoesNotExist:
            raise NotFound("Doctor not found")

        request.data['doctor']=doctor.id
        serializer=SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
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


class DoctorAvailableSlotsView(APIView):
    def get(self, request, doctor_id):
        try:
            user=UserProfile.objects.get(id=doctor_id)
            doctor=Doctor.objects.get(user_profile=user)

            slots = Slot.objects.filter(doctor=doctor.id, is_available=True)
            sorted_slots=slots.order_by('date','time')
            serializer = SlotSerializer(sorted_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SlotDelete(APIView):
    def delete(self,request,slot_id):
        try:
            slot=Slot.objects.get(id=slot_id)
            slot.delete()
        except Slot.DoesNotExist:
            return Response ({'data':"slot is not exist"},status=status.HTTP_404_NOT_FOUND)
        return Response({'data':'deleted'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_doctor_profile(request, doctor_id):
   
    user=UserProfile.objects.get(id=doctor_id)

    doctor = get_object_or_404(Doctor, user_profile=user)

    # Create a dictionary with the doctor's profile data
    doctor_profile_data = {
        'doctorName': doctor.doctor_name,
        'doctorImage': doctor.doctor_image.url,
        'department': doctor.doctor_department.name,
        'qualification': doctor.qualification.title,
        'fee': doctor.fee,
        'phone': doctor.phone,
        'address': str(doctor.address),
    }

    return Response(doctor_profile_data, status=status.HTTP_200_OK)
