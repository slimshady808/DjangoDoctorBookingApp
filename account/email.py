from django.core.mail import send_mail

from django.conf import settings
from .models import UserProfile


def send_otp_via_email(email,otp):
    subject="you account varification email "
    
    message=f"your otp is {otp}"
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    
def send_email_forgot_password(subject,message,recipient_list):
    print('email send to ',recipient_list)
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,recipient_list)