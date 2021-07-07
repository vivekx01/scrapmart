from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userinfo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dob=models.DateField()
    phone=models.CharField(max_length=12)
    securityquestion=models.CharField(max_length=50)
    securityanswer=models.CharField(max_length=100)