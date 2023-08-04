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
from .models import Doctor,Department,Address
from .serializers import DoctorSerializer,DepartmentSerializer,AddressSerializer,QualificationSerializer
from .backends import DoctorModelBackend
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from .models import Department, Qualification
# Create your views here.
User = get_user_model()

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'doctor/login',
        'doctor/register'
    ]
    return Response(routes)




class DoctorRegistrationView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Hash the password before saving the doctor
        password = request.data['password']
        hashed_password = make_password(password)
        serializer.save(password=hashed_password)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

class DoctorLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        doctor = DoctorModelBackend().authenticate(request, email=email, password=password)
        if doctor is not None:
            login(request, doctor)
            refresh = RefreshToken.for_user(doctor)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class DoctorList(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors,many=True)
        data=serializer.data

        for doctor in data:
            department_id=doctor['doctor_department']
            department=Department.objects.get(id=department_id)
            doctor['department_name']=department.name

        # department_name=department.name
        # for doctor in data:
        #     doctor['departmet_name']=department_name
        return Response(data, status=status.HTTP_200_OK)
    

    
@api_view(['GET'])
def get_doctors_by_department(request, department_id):
    try:
        doctors = Doctor.objects.filter(doctor_department=department_id)
        serializer = DoctorSerializer(doctors, many=True)
        data=serializer.data

        department = Department.objects.get(id=department_id)
        department_name = department.name
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
