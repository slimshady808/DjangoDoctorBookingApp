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
from .serializers import DoctorSerializer,DepartmentSerializer,AddressSerializer,QualificationSerializer,SlotSerializer
from .backends import DoctorModelBackend
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from .models import Department, Qualification
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone
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
    
class DoctorLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        doctor = DoctorModelBackend().authenticate(request, email=email, password=password)
        if doctor is not None:
            login(request, doctor)
            refresh = RefreshToken.for_user(doctor)
         
            # Customize the access token by adding custom claims
            access_token = refresh.access_token
            access_token_dict = access_token.payload
            
            # Add custom claims to the access token dictionary
            print(doctor.doctor_name)
            print( doctor.email)
            print( doctor.is_staff)
            access_token_dict['doctor_name'] = doctor.doctor_name
            access_token_dict['email'] = doctor.email
            access_token_dict['is_staff'] = doctor.is_staff

            # access_token = str(refresh.access_token)
            # refresh_token = str(refresh)
            return Response({'access': str(access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)






class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Get the refresh token from the request data
        refresh_token = request.data.get("refresh")

        # Attempt to verify the refresh token
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token_payload = refresh_token.payload
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the user from the payload of the original access token
        user_id = refresh_token_payload.get("user_id")
        user = get_user_model().objects.filter(id=user_id).first()

        if user:
            # Add custom claims to the new access token payload
            new_refresh = refresh_token.access_token
            new_refresh_payload = new_refresh.payload
            new_refresh_payload["doctor_name"] = user.doctor_name
            new_refresh_payload["email"] = user.email
            new_refresh_payload["is_staff"] = user.is_staff

            # Return the new access token and refresh token
            return Response(
                {"access": str(new_refresh), "refresh": str(refresh_token)},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)



# class MyTokenRefreshView(TokenRefreshView):
#     def get_serializer(self, *args, **kwargs):
#         # Get the default serializer
#         serializer = super().get_serializer(*args, **kwargs)

#         # Get the user from the context
#         user = self.request.user

#         # Add custom claims to the new access token dictionary
#         # serializer.payload['doctor_name'] = user.doctor_name
#         # serializer.payload['email'] = user.email
#         # serializer.payload['is_staff'] = user.is_staff

#         return serializer

# @api_view(['POST'])
# def refresh_access_token(request):
#     try:
#         refresh_token = request.data['refresh']
#         print(refresh_token)
#         refresh_view = TokenRefreshView.as_view()
#         response = refresh_view(request=request)
#         return Response(response.data, status=response.status_code)
#     except Exception as e:
#         return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
    


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

# @api_view(['GET'])
# def get_available_slots(request,doctor_id):
#     doctor=Doctor.objects.get(id=doctor_id)

#     selected_date = request.GET.get('date')
#     if not selected_date:
#         return Response({'error':'not a valid date'},status=status.HTTP_400_BAD_REQUEST)
#     try:
#         slots=doctor.get_available_slots_by_date(selected_date)
#         serializer=SlotSerializer(slots,many=True)
#         return Response({'available_slots':serializer.data},status=status.HTTP_200_OK)
    
#     except Exception as e :
#         return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
# @api_view(['GET'])
# def get_available_slots(request,doctorId):
#     try:
#         doctor=Doctor.objects.get(id=doctorId)
#         today = timezone.now().date()

#         slots=Slot.objects.filter(doctor=doctor,is_available=True, date__gte=today)

#         serializer= SlotSerializer(slots,many=True)

#         return Response (serializer.data,status=status.HTTP_200_OK)
#     except Slot.DoesNotExist:
#         return Response({'error':'slots does not exists'},status=status.HTTP_404_NOT_FOUND)
