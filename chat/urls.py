# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('user-to-doctor-messages/', views.UserToDoctorMessageListCreateView.as_view(), name='user-to-doctor-message-list'),
    path('user-to-doctor-messages/<int:pk>/', views.UserToDoctorMessageDetailView.as_view(), name='user-to-doctor-message-detail'),
    path('doctor-to-user-messages/', views.DoctorToUserMessageListCreateView.as_view(), name='doctor-to-user-message-list'),
    path('doctor-to-user-messages/<int:pk>/', views.DoctorToUserMessageDetailView.as_view(), name='doctor-to-user-message-detail'),
]
