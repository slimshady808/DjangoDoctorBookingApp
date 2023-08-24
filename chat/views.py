# chat/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import UserToDoctorMessage, DoctorToUserMessage
from .serializers import UserToDoctorMessageSerializer, DoctorToUserMessageSerializer

class CreateUserToDoctorMessage(generics.CreateAPIView):
    queryset=UserToDoctorMessage.objects.all()
    serializer_class=UserToDoctorMessageSerializer

class UserToDoctorMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserToDoctorMessage.objects.all()
    serializer_class = UserToDoctorMessageSerializer

class CreateDoctorToUserMessage(generics.CreateAPIView):
    queryset=DoctorToUserMessage.objects.all()
    serializer_class=DoctorToUserMessageSerializer

# class DoctorToUserMessageListCreateView(generics.ListCreateAPIView):
#     queryset = DoctorToUserMessage.objects.all()
#     serializer_class = DoctorToUserMessageSerializer

class DoctorToUserMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorToUserMessage.objects.all()
    serializer_class = DoctorToUserMessageSerializer




@api_view(['GET'])
def fetch_messages(request,  doctor_id ,user_id):
    # Fetch messages sent by the user to the doctor
    user_to_doctor_messages = UserToDoctorMessage.objects.filter(sender=user_id, receiver=doctor_id)

    # Fetch messages sent by the doctor to the user
    doctor_to_user_messages = DoctorToUserMessage.objects.filter(sender=doctor_id, receiver=user_id)

    # Combine and order the messages by timestamp
    all_messages = list(user_to_doctor_messages) + list(doctor_to_user_messages)
    all_messages.sort(key=lambda message: message.timestamp)

    # Serialize the messages and return the response
    serializer = UserToDoctorMessageSerializer(all_messages, many=True)
    
    return Response(serializer.data)

