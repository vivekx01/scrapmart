from django.db import models
import uuid
from django.conf import settings
User = settings.AUTH_USER_MODEL


# Create your models here.

class searchdb(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=20)
    locality=models.CharField(max_length=30)
    shopname=models.CharField(max_length=100)
    shopaddress=models.CharField(max_length=500)
    shopcontact=models.CharField(max_length=12)
    is_verified=models.BooleanField(default=False)