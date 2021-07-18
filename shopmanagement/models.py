from django.db import models


# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
class searchdb(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=20)
    locality=models.CharField(max_length=30)
    shopname=models.CharField(max_length=100)
    shopaddress=models.CharField(max_length=500)
    shopcontact=models.CharField(max_length=12)
    shopimage=models.ImageField(upload_to ='searchdb/')
    is_verified=models.BooleanField(default=False)