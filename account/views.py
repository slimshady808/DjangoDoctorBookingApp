from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from .email import send_otp_via_email,send_email_forgot_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
import random
import jwt
from .serializers import ResetPasswordSerializer
from .serializers import UserProfileSerializer,PatientSerializer
from .models import UserProfile,Patient
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
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

class ResetPasswordView(APIView):
    def post(self,request):
        serializer=ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            # decode the jwt token to access the payload
            try:
                payload=jwt.decode(request.auth.token,settings.SECRET_KEY,algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({'error':'token has expired'},status=status.HTTP_401_UNAUTHORIZED)
            except jwt.DecodeError:
                return Response({'error':'invalid token'},status=status.HTTP_401_UNAUTHORIZED)
            
            user_role=payload.get('role')
            if user_role != 'doctor':
                return Response({'erorr':'user is not a doctor'},status=status.HTTP_403_FORBIDDEN)
            
            user_id = payload.get('user_id')

            old_password=serializer.validated_data['old_password']
            new_password=serializer.validated_data['new_password']
            
            user=UserProfile.objects.get(id=user_id)
            if user.check_password(old_password):
                #update password
                user.set_password(new_password)
                print('new password is ',new_password)
                user.save()
                return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
            else :
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ForgotPassword(request):   
    email=request.data.get('email')
    try:
        user=UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return Response({"status":400,"message":"no user is available for that email"})
    # generate  a unique token for the password reset request
    token_generator=PasswordResetTokenGenerator()
    token=token_generator.make_token(user)

    #Encode the user's email and token for the reset link
    uidb64=urlsafe_base64_encode(force_bytes(user.pk))
  

    #Build the reset link URL
    reset_link= reverse('password_reset_confirm',kwargs={'uidb64':uidb64,'token':token})
    reset_link=f'http://{get_current_site(request).domain}{reset_link}'

    #send a password reset email

    subject='password reset request'
    message= f'Click the following link to reset your password:\n\n{reset_link}'
    recipient_list=[user.email]

    try:
        send_email_forgot_password(subject,message,recipient_list)
        return Response({"status": 200, "message": "Password reset link sent successfully"})
    except Exception as e:
        return Response({"status": 500, "message": "An error occurred while sending the reset link"})
    

            


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

    