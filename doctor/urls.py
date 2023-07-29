from django.urls import path
from . import views
from .views import DoctorRegistrationView, DoctorLoginView, DoctorProfileView
urlpatterns = [
    path('', views.getRoutes),
    path('register/', DoctorRegistrationView.as_view(), name='doctor-register'),
    path('login/', DoctorLoginView.as_view(), name='doctor-login'),
    path('profile/', DoctorProfileView.as_view(), name='doctor-profile'),
]