from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

# Create your models here.
class userinfo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dob=models.DateField()
    phone=models.CharField(max_length=12)
    securityquestion=models.CharField(max_length=50)
    securityanswer=models.CharField(max_length=100)