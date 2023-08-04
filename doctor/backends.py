# doctorapp/backends.py

from django.contrib.auth.backends import BaseBackend


from django.contrib.auth import get_user_model

User = get_user_model()

class DoctorModelBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            print("Attempting authentication for email:", email)
            doctor = User.objects.get(email=email)
            if doctor.is_active and doctor.check_password(password):
                print("Authentication successful for email:", email)
                doctor.backend = 'doctor.backends.DoctorModelBackend'
                return doctor
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


















# from .models import Doctor

# class DoctorModelBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None):
#         try:
#             doctor = Doctor.objects.get(email=email)
#             if doctor.check_password(password):
#                 return doctor
#         except Doctor.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Doctor.objects.get(pk=user_id)
#         except Doctor.DoesNotExist:
#             return None
