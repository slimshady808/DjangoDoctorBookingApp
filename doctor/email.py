from django.core.mail import send_mail
from django.conf import settings

def send_email(user_data):
    email_subject = "Congratulations! Your Doctor Account has been created"
    email_message = (
        f"Dear {user_data['username']},\n\n"
        f"Congratulations! Your doctor account has been successfully created.\n"
        f"Here are your login details:\n\n"
        f"email: {user_data['email']}\n"
        f"Temporary Password: newpassword\n\n"
        f"Please login with your email and the provided temporary password.\n"
        f"Once logged in, you will be prompted to set a strong password of your choice.\n\n"
        f"Thank you for joining our platform!\n\n"
        f"Best regards,\nYour Application Team"
    )

    recipient_list = [user_data["email"]]
    email_from = settings.EMAIL_HOST

    send_mail(email_subject, email_message, email_from, recipient_list)
