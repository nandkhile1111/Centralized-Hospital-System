from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.hashers import make_password

# Create your models here.


class Hospitals(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE)
    hname = models.CharField(max_length=100)
    himage = models.ImageField(upload_to="hospitalimage/")
    hnumber = models.BigIntegerField(null = True)
    hopentime = models.TimeField(null = True)
    hclosetime = models.TimeField(null = True)
    hemail=models.EmailField(null=True)
    
    
    

    def __str__(self):
        return self.hname
    
class Doctors(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE)
    dname = models.CharField(max_length=100)
    ddob = models.DateField()
    ddegree = models.CharField(max_length = 100)
    dspecialization = models.CharField(max_length = 100)
    dage = models.IntegerField(default = 0)

    def __str__(self):
        return self.dname

    def save(self, *args, **kwargs):
        self.ddob = datetime.strptime(str(self.ddob), '%Y-%m-%d').date()
        today = datetime.now().date()
        dage = today.year - self.ddob.year - ((today.month, today.day) < (self.ddob.month, self.ddob.day))
        self.dage = dage

        super().save(*args, **kwargs)

class Specialties(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE)
    sname = models.CharField(max_length = 100)
    simage = models.ImageField(upload_to="specialtiesimages/")
    sabout = models.TextField()

class AboutHospital(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE)
    ahimage = models.ImageField(upload_to="abouthospitalimage/")
    ahintroduction = models.TextField()
    ahvision = models.TextField()
    ahmission = models.TextField()

class HospitalAddress(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE)
    ahname = models.TextField(null=True)
    ahbname = models.TextField()
    ahsname = models.TextField()
    ahcname = models.TextField()
    ahpostalcode =models.BigIntegerField()  

    def __str__(self):
        return self.ahname      

class Contactus(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE) 
    name = models.CharField(max_length = 100)
    email = models.EmailField() 
    subject = models.TextField()
    message = models.TextField()  
    hid = models.CharField(max_length =50,null=True)  # in hid  we store the hospital userid which is get by session 

class Treatment(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE) 
    tname = models.CharField(max_length = 100)
    tcharge = models.BigIntegerField() 
    tinfo = models.TextField()

class Appointment(models.Model):
    uhid = models.ForeignKey(User , on_delete=models.CASCADE) 
    hid = models.CharField(max_length =50)  # in hid  we store the hospital userid which is get by session 
    doctorname = models.CharField(max_length = 50)
    disease = models.CharField(max_length =100)
    pname = models.CharField(max_length =100)
    pnumber = models.BigIntegerField()
    hname = models.CharField(max_length = 100, null = True)

                       


    