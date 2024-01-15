from django.contrib import admin
from CentralizedHospitalApp.models import  Hospitals,Doctors,Specialties,AboutHospital,HospitalAddress

from django.contrib.auth.models import User
# Register your models here.




class HospitalName(admin.ModelAdmin):
    list_display = ['id','uhid','hname','himage']

admin.site.register(Hospitals,HospitalName)

class DoctorsName(admin.ModelAdmin):
    list_display = ['dname','ddob','ddegree','dspecialization','dage']
    
admin.site.register(Doctors,DoctorsName)

class HospitalAddressName(admin.ModelAdmin):
    list_display = ['ahbname','ahsname','ahcname','uhid','ahpostalcode']
    
admin.site.register(HospitalAddress,HospitalAddressName)


    
     


