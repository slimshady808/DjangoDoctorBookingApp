from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
urlpatterns = [
    path('', views.getRoutes),
    path('token/', views.MytokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.Registerview.as_view()),
    path('verify-otp/', views.OTPVerification.as_view(), name='verify-otp'),
    path('user-list/', views.userList, name='user-list'),
    path('patients/<int:userId>/',views.get_patients,name='patients'),
    path('create-patient/',views.PatientCreateView.as_view(),name='create-patient'),
    path('reset-password/',views.ChangePasswordView.as_view(),name='reset-password'),


    path('forgot-password/',views.ForgotPassword,name='forgot-password'),
    path('new-password/',views.reset_password,name='reset-password'),
    path('block-user/<int:user_id>/',views.BlockUserView.as_view())

]