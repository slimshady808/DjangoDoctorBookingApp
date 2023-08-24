# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('user-to-doctor-messages/', views.CreateUserToDoctorMessage.as_view(), name='user-to-doctor-message-list'),
    path('user-to-doctor-messages/<int:pk>/', views.UserToDoctorMessageDetailView.as_view(), name='user-to-doctor-message-detail'),
    path('doctor-to-user-messages/', views.CreateDoctorToUserMessage.as_view(), name='doctor-to-user-message-list'),
    path('doctor-to-user-messages/<int:pk>/', views.DoctorToUserMessageDetailView.as_view(), name='doctor-to-user-message-detail'),
    path('fetch-messages/<int:doctor_id>/<int:user_id>/', views.fetch_messages, name='messages')
]
