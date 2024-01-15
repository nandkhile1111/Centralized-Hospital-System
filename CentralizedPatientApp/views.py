from django.shortcuts import render,redirect
from CentralizedPatientApp.models import Patient
from CentralizedHospitalApp.models import Hospitals,HospitalAddress,Doctors,AboutHospital,Specialties
from django.contrib import messages
# Create your views here.
def userindexpage(request):
    d=request.user.id
    pdata = Patient.objects.filter(upid_id = d)
    hdata = Hospitals.objects.all()
    return render(request,"userindexpage.html",{'pdata':pdata,'hdata':hdata}) 

def adduserinfo(request):
    if request.method == 'POST':
        pname = request.POST['pname']
        pdob = request.POST['pdob']
        pphone= request.POST['pphone']
        pemail = request.POST['pemail']
        paddress = request.POST['paddress']
        upid_id = request.user.id
        

        data = Patient.objects.create(
            pname=pname,
            pdob=pdob,
            pphone=pphone,
            pemail = pemail,
            paddress=paddress,
            upid_id = upid_id
        ) 
        data.save()
        messages.success(request,"Information added successfully")
        return redirect("/adduserinfo")
    else:
        return render(request,"adduserinfo.html") 
    
def index(request,id):
    #request.session['hid']=id   # create a session to store  the hosital  so we can use that id to look look some particular hospital data
    
    hdata = Hospitals.objects.filter(uhid_id = id )  #send hospital data like name time email in each page by adding these lline innall functions
    hadata = HospitalAddress.objects.filter(uhid_id = id)
    print(hdata)
    return render(request,'index.html',{'hdata':hdata,'hadata':hadata})
    
def listabouthospital(request,id):
    request.session['hid']=id   # access the session which is created in index function in centralizedPatientApp to access the information of particular hospital
    
    hdata = Hospitals.objects.filter(uhid_id = id )     # particular hospital data
    ahdata = AboutHospital.objects.filter(uhid_id = id)      # hospital about data in  hospital
    ddata = Doctors.objects.filter(uhid = id)               # get the doctors in particular hospital
    sdata = Specialties.objects.filter(uhid = id) 
    hadata = HospitalAddress.objects.filter(uhid_id = id)


    return render(request,'listabouthospital.html',{'hdata':hdata, 'ahdata':ahdata,'ddata': ddata,'sdata':sdata,'hadata':hadata})

