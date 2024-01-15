from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Patient(models.Model):
    upid = models.ForeignKey(User , on_delete=models.CASCADE)
    pname= models.CharField(max_length= 100)
    pdob = models.DateField()
    pphone = models.BigIntegerField()
    pemail = models.EmailField()
    paddress = models.TextField()