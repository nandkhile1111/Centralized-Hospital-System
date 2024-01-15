from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from CentralizedHospitalApp.models import Hospitals,Doctors,Specialties,AboutHospital,HospitalAddress,Contactus,Treatment,Appointment
from CentralizedPatientApp.models import Patient

# Create your views here.
def handlelogin(request):
    if request.method == 'POST':

        username = request.POST['username']
        password= request.POST['password']
        print(username)
    
       
        myuser = authenticate(username = username , password = password)
        
        print(request.user.is_staff)
        if myuser is not None :
            if myuser.is_staff:
                login(request,myuser)
                return redirect("/index")
                
                
            else:
                login(request,myuser)
                return redirect("/userindexpage")
                
        
        else:
            messages.success(request,"You are not Authorized yet")
            return redirect("/handlelogin")

    return render(request,'handlelogin.html')

def register(request):
    if request.method=="POST":
        
        username = request.POST['username']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        usertype = request.POST['usertype']

        if username == "" or password =="" or confirm_password == "":
            messages.warning(request,"Field is not be Empty")
            return render(request,'register.html')

        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'register.html')
        

        try:
            if User.objects.get(username=username):
               
                messages.error(request,"Username is Taken")
                return render(request,'register.html')
        except Exception as identifier:
            pass



        user = User.objects.create(
            
            username = username,
            usertype = usertype
        
        )
        user.set_password(password)
        user.is_active=False
        user.save()
        messages.error(request,"Regestrarion Successful")
    return render(request,'register.html')

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Successfully")
    return redirect("/handlelogin")

def index(request):
    d=request.user.id
    print(d)
    
    hdata = Hospitals.objects.filter(uhid_id = d )  #send hospital data like name time email in each page by adding these lline innall functions
    hadata = HospitalAddress.objects.filter(uhid_id = d)
    print(hdata)
    return render(request,'index.html',{'hdata':hdata,'hadata':hadata})

def adddoctors(request):
    if request.method == 'POST':
        dname = request.POST['dname']
        ddob = request.POST['ddob']
        ddegree = request.POST['ddegree']
        dspecialization = request.POST['dspecialization']
        uhid_id = request.user.id
        

        data = Doctors.objects.create(
            dname=dname,
            ddob=ddob,
            ddegree=ddegree,
            dspecialization = dspecialization,
            uhid_id = uhid_id
        ) 
        data.save()
        messages.success(request,"Doctor added successfully")
        return redirect("/adddoctors")
    
    else:
    
        d=request.user.id
        hdata = Hospitals.objects.filter(uhid_id = d )
        hadata = HospitalAddress.objects.filter(uhid_id = d)
        return render(request,'adddoctors.html',{'hdata':hdata,'hadata':hadata})

def listdoctors(request):
    hid = request.session.get('hid')   # access the session which is created in index function in centralizedPatientApp to access the information of particular hospital
    
    

    if request.user.is_staff:
        # If the user is staff (hospital), get data related to the hospital
        d = request.user.id 
        hdata = Hospitals.objects.filter(uhid_id=d)
        ddata = Doctors.objects.filter(uhid_id=d)
        hadata = HospitalAddress.objects.filter(uhid_id=d)

    else:
        # If the user is not staff, assume it's a regular user, and get data related to the user
        hdata = Hospitals.objects.filter(uhid_id=hid)
        ddata = Doctors.objects.filter(uhid_id=hid)
        hadata = HospitalAddress.objects.filter(uhid_id=hid)
    

    return render(request,'listdoctors.html',{'hdata':hdata, 'ddata':ddata,'hadata':hadata})

def updatedoctor(request,id):
    if request.method =='POST':
        dname = request.POST['dname']
        ddob = request.POST['ddob']
        ddegree = request.POST['ddegree']
        dspecialization = request.POST['dspecialization']

        data=Doctors.objects.get(pk=id)

        
        data.dname=dname
        data.ddob=ddob
        data.ddegree=ddegree
        data.dspecialization=dspecialization

        data.save()
    

        return redirect("/listdoctors")
    else:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )   # particular hospital data
        ddata = Doctors.objects.filter(uhid_id =d)    # all doctors data in particular hospital
        pddata = Doctors.objects.filter(pk = id)      # get a data of particular doctor in hospital
        hadata = HospitalAddress.objects.filter(uhid_id = d)

        return render(request,'updatedoctors.html',{'hdata':hdata, 'ddata':ddata, 'pddata':pddata,'hadata':hadata})
    

def deletedoctor(request,id):
    
    d=request.user.id                        # get the id of login hospital Hospital
    hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
    ddata = Doctors.objects.filter(uhid_id =d)      # doctors data in particular hospital
    doctor = Doctors.objects.filter(pk = id)    # get the data of doctor which you want to delete
    doctor.delete()
    
    return render(request,'listdoctors.html',{'hdata':hdata, 'ddata':ddata})


def addspecialties(request):
    if request.method == 'POST':
        sname = request.POST['sname']
        sabout = request.POST['sabout']
        simage = request.FILES.get('simage')
       
        uhid_id = request.user.id
        

        data = Specialties.objects.create(
            sname=sname,
            sabout=sabout,
            simage=simage,
            
            uhid_id = uhid_id
        ) 
        data.save()
        messages.success(request,"Speciality added successfully")

        return redirect("/addspecialties")
    
    else:
    
        d=request.user.id
        hdata = Hospitals.objects.filter(uhid_id = d )
        hadata = HospitalAddress.objects.filter(uhid_id = d)

        return render(request,'addspecialties.html',{'hdata':hdata,'hadata':hadata})


def listspecialties(request):
    hid = request.session.get('hid')   # access the session which is created in index function in centralizedPatientApp to access the information of particular hospital
    if request.user.is_staff:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
        sdata = Specialties.objects.filter(uhid_id =d)      # specialties data in particular hospital
        hadata = HospitalAddress.objects.filter(uhid_id = d)
    else:
        hdata = Hospitals.objects.filter(uhid_id = hid )     # particular hospital data
        sdata = Specialties.objects.filter(uhid_id = hid)      # specialties data in particular hospital
        hadata = HospitalAddress.objects.filter(uhid_id = hid)

    return render(request,'listspecialties.html',{'hdata':hdata, 'sdata':sdata,'hadata':hadata})

def aboutspecialties(request,id):
    hid = request.session.get('hid')   # access the session which is created in index function in centralizedPatientApp to access the information of particular hospital

    if request.user.is_staff:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
        psdata = Specialties.objects.filter(pk = id)      # perticular specialtiess data in particular hospital
        hadata = HospitalAddress.objects.filter(uhid_id = d)
    else:
        hdata = Hospitals.objects.filter(uhid_id = hid )     # particular hospital data
        psdata = Specialties.objects.filter(pk = id)      # perticular specialtiess data in particular hospital
        hadata = HospitalAddress.objects.filter(uhid_id = hid)
    return render(request,'aboutspecialties.html',{'hdata':hdata, 'psdata':psdata,'hadata':hadata})

def updatespecialties(request,id):
    if request.method =='POST':
        sname = request.POST['sname']
        sabout = request.POST['sabout']
        simage = request.FILES.get('simage')
        
        data = Specialties.objects.get(pk = id)
        if simage is None:
            simage = data.simage 

        data.sname = sname
        data.sabout = sabout
        data.simage = simage 
        data.save()

        return redirect("/listspecialties")
    else:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
        psdata = Specialties.objects.filter(pk = id)      # perticular specialtiess data in particular hospital
        hadata = HospitalAddress.objects.filter(uhid_id = d)

        return render(request,'updatespecialties.html',{'hdata':hdata, 'psdata':psdata,'hadata':hadata})

def addabouthospital(request):
    if request.method == 'POST':
        ahintroduction= request.POST['ahintroduction']
        ahvision = request.POST['ahvision']
        ahmission = request.POST['ahmission']
        ahimage = request.FILES.get('ahimage')
       
        uhid_id = request.user.id
        

        data = AboutHospital.objects.create(
            ahintroduction=ahintroduction,
            ahvision=ahvision,
            ahmission=ahmission,
            ahimage=ahimage,
            
            uhid_id = uhid_id
        ) 
        data.save()
        messages.success(request,'Information added successfully')
        return redirect("/addabouthospital")
    else:
        d=request.user.id
        hdata = Hospitals.objects.filter(uhid_id = d )
        hadata = HospitalAddress.objects.filter(uhid_id = d)

        return render(request,'addabouthospital.html',{'hdata':hdata,'hadata':hadata})
    

def addabouthospitalinfo(request):
    if request.method == 'POST':
        hname= request.POST['hname']
        himage = request.FILES.get('himage')
        hnumber = request.POST['hnumber']
        hopentime = request.POST['hopentime']
        hclosetime =request.POST['hclosetime']
        hemail =request.POST['hemail']
       
        uhid_id = request.user.id

        data = Hospitals.objects.create(
            hname=hname,
            himage=himage,
            hnumber=hnumber,
            hopentime=hopentime,
            hclosetime=hclosetime,
            hemail=hemail,
            
            uhid_id = uhid_id
        )
        data.save()
        messages.success(request,'Information added successfully')
        return redirect("/addabouthospitalinfo")
    else:   
        d=request.user.id
        hdata = Hospitals.objects.filter(uhid_id = d )
        hadata = HospitalAddress.objects.filter(uhid_id = d)

        return render(request,'addabouthospitalinfo.html',{'hdata':hdata,'hadata':hadata})
    
def updateabouthospitalinfo(request):
    if request.method == 'POST':
        hname= request.POST['hname']
        himage = request.FILES.get('himage')
        hnumber = request.POST['hnumber']
        hopentime = request.POST['hopentime']
        hclosetime =request.POST['hclosetime']
        hemail =request.POST['hemail']
       
        uhid_id = request.user.id
        data = Hospitals.objects.get(uhid_id = uhid_id)
        if himage is None:
            himage = data.himage 

        if not hopentime:
            hopentime = data.hopentime

        if not hclosetime:
            hclosetime = data.hclosetime


        data.hname=hname
        data.himage=himage
        data.hnumber=hnumber
        data.hopentime=hopentime
        data.hclosetime=hclosetime
        data.hemail=hemail
       
        data.save()
        messages.success(request,'Information added successfully')
        return redirect("/updateabouthospitalinfo")
    else:   
        d=request.user.id
        hdata = Hospitals.objects.filter(uhid_id = d )
        hadata = HospitalAddress.objects.filter(uhid_id = d)

        return render(request,'updateabouthospitalinfo.html',{'hdata':hdata,'hadata':hadata})
    
def listabouthospital(request):
    hid = request.session.get('hid')   # access the session which is created in index function in centralizedPatientApp to access the information of particular hospital
    if request.user.is_staff:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
        ahdata = AboutHospital.objects.filter(uhid_id =d)      # hospital about data in  hospital
        ddata = Doctors.objects.filter(uhid = d)               # get the doctors in particular hospital
        sdata = Specialties.objects.filter(uhid = d) 
        hadata = HospitalAddress.objects.filter(uhid_id = d)
    else:
        hdata = Hospitals.objects.filter(uhid_id = hid )     # particular hospital data
        ahdata = AboutHospital.objects.filter(uhid_id = hid)      # hospital about data in  hospital
        ddata = Doctors.objects.filter(uhid = hid)               # get the doctors in particular hospital
        sdata = Specialties.objects.filter(uhid = hid) 
        hadata = HospitalAddress.objects.filter(uhid_id = hid)


    return render(request,'listabouthospital.html',{'hdata':hdata, 'ahdata':ahdata,'ddata': ddata,'sdata':sdata,'hadata':hadata})

def addaddresshospital(request):
    if request.method == 'POST':
        ahbname= request.POST['ahbname']
        ahsname = request.POST['ahsname']
        ahcname = request.POST['ahcname']
        ahpostalcode = request.POST['ahpostalcode']

        uhid_id = request.user.id

        data = HospitalAddress.objects.create(
            ahbname=ahbname,
            ahsname=ahsname,
            ahcname=ahcname,
            ahpostalcode=ahpostalcode,
            
            uhid_id = uhid_id
        ) 
        data.save()
        messages.success(request,'Address added successfully')
        return redirect("/addaddresshospital")
        
    else:
        d=request.user.id
        hdata = Hospitals.objects.filter(uhid_id = d )
        hadata = HospitalAddress.objects.filter(uhid_id = d)

        return render(request,'addaddresshospital.html',{'hdata':hdata,'hadata':hadata})
    
def contactus(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        email = request.POST['uemail']
        subject = request.POST['usubject']
        message = request.POST['umessage']

        uhid_id = request.user.id
        hid = request.session.get('hid')

        if not request.user.is_staff:

            data = Contactus.objects.create(
                name=uname,
                email=email,
                subject=subject,
                message=message,
                uhid_id=uhid_id,
                hid= hid
            )
            data.save()
            messages.success(request, 'Message sent successfully')
            return redirect("/contactus")

    else:
        hid = request.session.get('hid')
        if request.user.is_staff:
            d = request.user.id
            hdata = Hospitals.objects.filter(uhid_id=d)
            hadata = HospitalAddress.objects.filter(uhid_id=d)
        else:
            hdata = Hospitals.objects.filter(uhid_id=hid)
            hadata = HospitalAddress.objects.filter(uhid_id=hid)

    return render(request, 'contactus.html', {'hdata': hdata, 'hadata': hadata})

    
def contactusmessages(request):
    d=request.user.id                        # get the id of login hospital Hospital
    hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
    cdata = Contactus.objects.filter(hid =d)      # get the messages data of particular hospital
    hadata = HospitalAddress.objects.filter(uhid_id = d)
 
    
    return render(request,'contactusmessages.html',{'hdata':hdata, 'cdata':cdata,'hadata':hadata})


def addtreatments(request):
    if request.method == 'POST':
        tname= request.POST['tname']
        tcharge= request.POST['tcharge']
        tinfo= request.POST['tinfo']

        uhid_id = request.user.id

        data = Treatment.objects.create(
            tname=tname,
            tcharge=tcharge,
            tinfo=tinfo,

            uhid_id = uhid_id
        )

        data.save()
        messages.success(request,'Treatment added successfully')
        return redirect("/addtreatments")
    else:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
        
        hadata = HospitalAddress.objects.filter(uhid_id = d)
 
    
        return render(request,'addtreatments.html',{'hdata':hdata, 'hadata':hadata})
    

def listtreatments(request):
    hid = request.session.get('hid')   # access the session which is created in index function in centralizedPatientApp to access the information of particular hospital
    if request.user.is_staff:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
        hadata = HospitalAddress.objects.filter(uhid_id = d)
        tdata = Treatment.objects.filter(uhid_id =d)
    else:
        hdata = Hospitals.objects.filter(uhid_id = hid )     # particular hospital data
        hadata = HospitalAddress.objects.filter(uhid_id = hid)
        tdata = Treatment.objects.filter(uhid_id = hid)

    return render(request,'listtreatments.html',{'hdata':hdata, 'hadata':hadata,'tdata':tdata})


def updatetreatments(request,id):
    if request.method =='POST':
        tname= request.POST['tname']
        tcharge= request.POST['tcharge']
        tinfo= request.POST['tinfo']
        


        data=Treatment.objects.get(pk=id)

        data.tname= tname
        data.tcharge= tcharge
        data.tinfo= tinfo

        

        data.save()
    

        return redirect("/listtreatments")
    else:
        d=request.user.id                        # get the id of login hospital Hospital
        hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
        hadata = HospitalAddress.objects.filter(uhid_id = d)
        tdata = Treatment.objects.filter(uhid_id =d)

        return render(request,'updatetreatments.html',{'hdata':hdata, 'hadata':hadata,'tdata':tdata})
    
def deletetreatments(request,id):

    d=request.user.id                        # get the id of login hospital Hospital
    hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
    hadata = HospitalAddress.objects.filter(uhid_id = d)
    tdata = Treatment.objects.filter(uhid_id =d)      
    treatment = Treatment.objects.filter(pk=id) 
    treatment.delete()
    
    return render(request,'listtreatments.html',{'hdata':hdata, 'hadata':hadata,'tdata':tdata})
   
def makeappointment(request):
    hid = request.session.get('hid')   # access the session which is created in index function in centralizedPatientApp to access the information of particular hospital

    if request.method == 'POST':
        pname = request.POST['pname']
        pnumber = request.POST['pnumber']
        disease = request.POST['disease']
        doctorname = request.POST['doctorname']

        uhid_id = request.user.id
        hname = Hospitals.objects.get(uhid_id =hid).hname
        print(hname)
        data = Appointment.objects.create(
            pname = pname,
            pnumber = pnumber,
            disease =disease,
            doctorname = doctorname,
            uhid_id = uhid_id,
            hid = hid,
            hname=hname
        )
        data.save()
        messages.success(request,"Appointment added successfully")
        return redirect("/makeappointment")


    else:
        d=request.user.id 
        hdata = Hospitals.objects.filter(uhid_id = hid )     # particular hospital data
        hadata = HospitalAddress.objects.filter(uhid_id = hid)
        ddata = Doctors.objects.filter(uhid_id =hid)
        pdata = Patient.objects.filter(upid = d)
        
    return render(request,'makeappointment.html',{'hdata':hdata, 'hadata':hadata, 'ddata':ddata,'pdata':pdata})

def viewappointment(request):

    d=request.user.id 
    hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
    hadata = HospitalAddress.objects.filter(uhid_id = d)
    adata = Appointment.objects.filter(hid = d)
        
    return render(request,'viewappointment.html',{'hdata':hdata, 'hadata':hadata, 'adata':adata})


def appointmenthistory(request):

    d=request.user.id 
    hdata = Hospitals.objects.filter(uhid_id = d )     # particular hospital data
    hadata = HospitalAddress.objects.filter(uhid_id = d)
    adata = Appointment.objects.filter(uhid_id = d)
        
    return render(request,'appointmenthistory.html',{'hdata':hdata, 'hadata':hadata, 'adata':adata})
    
