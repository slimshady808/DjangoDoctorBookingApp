# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
      path('', views.getRoutes),
      path('create/',views.MessageCreateView.as_view(),name='message-create'),
      path('chat/<int:user_id>/<int:doctor_id>/', views.UserDoctorChatView.as_view(), name='user-doctor-chat'),

]

