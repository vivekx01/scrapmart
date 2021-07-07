from django.db import models

# Create your models here.
class userquery(models.Model):
    email=models.CharField(max_length=50)
    username=models.CharField(max_length=100)
    query=models.CharField(max_length=5000)
    status=models.BooleanField(default=False)