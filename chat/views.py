# chat/views.py

from rest_framework import generics
from .models import UserToDoctorMessage, DoctorToUserMessage
from .serializers import UserToDoctorMessageSerializer, DoctorToUserMessageSerializer

class UserToDoctorMessageListCreateView(generics.ListCreateAPIView):
    queryset = UserToDoctorMessage.objects.all()
    serializer_class = UserToDoctorMessageSerializer

class UserToDoctorMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserToDoctorMessage.objects.all()
    serializer_class = UserToDoctorMessageSerializer

class DoctorToUserMessageListCreateView(generics.ListCreateAPIView):
    queryset = DoctorToUserMessage.objects.all()
    serializer_class = DoctorToUserMessageSerializer

class DoctorToUserMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorToUserMessage.objects.all()
    serializer_class = DoctorToUserMessageSerializer

