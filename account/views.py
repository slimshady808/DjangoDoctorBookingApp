from django.shortcuts import render
from rest_framework.response import Response
from .email import send_otp_via_email
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
import random
from .serializers import UserProfileSerializer,PatientSerializer
from .models import UserProfile,Patient
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh'
    ]
    return Response(routes)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token= super().get_token(user)

        token['username']=user.username
        token['role']=user.user_type
        token['email'] = user.email

        return token

class MytokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
    
class Registerview(APIView):
    def post (self,request):
        
        serializer=UserProfileSerializer(data=request.data)
    
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_active'] = False
        password = make_password(request.data['password'])
        otp=str(random.randint(1000,9999))
        serializer.validated_data['otp']=otp
        serializer.save(password=password)
        send_otp_via_email(serializer.data['email'],otp)
        return Response ({
            "data":serializer.data,
            "status":201,
            "message":"registration successfully check email"
            })

class OTPVerification(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp_entered=request.data.get('otp')
        try:
            user_profile=UserProfile.objects.get(email=email)
            user_profile.is_active=True
            user_profile.otp=None
            user_profile.save()

            return Response({"status":200,
                             "message":"email verified successfully"})
        except UserProfile.DoesNotExist:
            return Response({
                "status":400,
                "message":"invalid OTP or email"
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def userList(request):
    users=UserProfile.objects.filter(user_type='user')
    serializer=UserProfileSerializer(users,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_patients(request,userId):
    try:
        patients=Patient.objects.filter(user_profile=userId)
        serializer=PatientSerializer(patients,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({'details':"patient not found"},status=status.HTTP_404_NOT_FOUND)
  
class PatientCreateView(CreateAPIView):
    queryset=Patient.objects.all()
    serializer_class=PatientSerializer

    