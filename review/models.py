from django.db import models
from doctor.models import Doctor
from account.models import User
# Create your models here.


class Review(models.Model):
    content=models.TextField()
    rating=models.IntegerField()
    doctor= models.ForeignKey(Doctor,on_delete=models.CASCADE)
    is_show=models.BooleanField(default=True)
    created_at= models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'doctor'] 


    def __str__(self):
        return f"Review by {self.user} for {self.doctor}"

