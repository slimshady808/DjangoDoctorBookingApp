from django.db import models
from account.models import User
from doctor.models import Doctor

class UserToDoctorMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sent_messages")
    receiver = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_received_messages")
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender} to {self.receiver}"

class DoctorToUserMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_received_messages")
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender} to {self.receiver}"

