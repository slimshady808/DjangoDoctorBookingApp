# from doctor.backends import DoctorModelBackend
# from account.authentication import EmailModelBackend

# class CustomAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Try to authenticate using the DoctorModelBackend
#         doctor_backend = DoctorModelBackend()
#         doctor_user = doctor_backend.authenticate(request=request)

#         if doctor_user:
#             # If authentication is successful, set the user in the request
#             request.user = doctor_user
#         else:
#             # If doctor authentication fails, fall back to the EmailModelBackend
#             email_backend = EmailModelBackend()
#             user = email_backend.authenticate(request=request)

#             # Set the user in the request, whether it's a doctor or a regular user
#             request.user = user

#         response = self.get_response(request)
#         return response



from doctor.backends import DoctorModelBackend
from account.authentication import EmailModelBackend

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to authenticate using the DoctorModelBackend
        doctor_backend = DoctorModelBackend()
        doctor_user = doctor_backend.authenticate(request=request)

        if doctor_user:
            # If authentication is successful, set the user in the request
            request.user = doctor_user
            print("Doctor authentication successful for email:", request.user.email)
        else:
            # If doctor authentication fails, fall back to the EmailModelBackend
            email_backend = EmailModelBackend()
            user = email_backend.authenticate(request=request)

            # Set the user in the request, whether it's a doctor or a regular user
            request.user = user if user and user.is_active else None
            if request.user:
                print("Email authentication successful for email:", request.user.email)
            else:
                print("Authentication failed for email:", request.POST.get("email"))

        print("Authentication middleware - Authenticated user:", request.user)

        response = self.get_response(request)
        return response

