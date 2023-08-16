from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer,PatientSerializer

from .models import User,Patient

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_admin'] = user.is_admin
        token['email'] = user.email
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh'
    ]
    return Response(routes)

@api_view(['GET'])
def userList(request):
    
    users = User.objects.filter(is_superuser=False)
    serializer = UserSerializer(users, many=True)
    
    return Response(serializer.data)


from django.contrib.auth.hashers import make_password

class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set the password using make_password to hash it before saving the user
        password = make_password(request.data['password'])
        serializer.save(password=password)

        return Response(serializer.data)

@api_view(['GET'])
def get_patients(request,userId):
    
    try:
        patients=Patient.objects.filter(user=userId)
        serializer=PatientSerializer(patients,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({'details':'patients not found'},status=status.HTTP_404_NOT_FOUND)



class PatientCreateView(CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer




@api_view(['POST'])
def create_booking(request):
    print(request.data)
    return Response({'message':'good'},status=201)