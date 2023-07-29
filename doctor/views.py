from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .models import Doctor
from .serializers import DoctorSerializer
from .backends import DoctorModelBackend
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh'
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
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)





# class DoctorLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         try:
#             doctor = Doctor.objects.get(email=email)

#             if not doctor.check_password(password):
#                 return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#             refresh = RefreshToken.for_user(doctor)
#             access_token = str(refresh.access_token)

#             return Response({'access_token': access_token}, status=status.HTTP_200_OK)

#         except Doctor.DoesNotExist:
#             return Response({'detail': 'No user found with this email'}, status=status.HTTP_404_NOT_FOUND)


class DoctorProfileView(APIView):
    def get(self, request):
        doctor = Doctor.objects.all()
        serializer = DoctorSerializer(doctor,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# @api_view(['GET'])
# def userList(request):
    
#     users = Doctor.objects.filter(is_superuser=False)
#     serializer = DoctorSerializer(users, many=True)
    
#     return Response(serializer.data)
