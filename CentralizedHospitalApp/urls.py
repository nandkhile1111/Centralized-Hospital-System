

from django.urls import path,include
from CentralizedHospitalApp import views
urlpatterns = [

    path('',views.handlelogin),
    path('handlelogin',views.handlelogin),
    path('handlelogout',views.handlelogout),
    path('register',views.register),
    path('index',views.index),
    path('adddoctors',views.adddoctors),
    path('listdoctors',views.listdoctors),
    path('updatedoctor/<id>',views.updatedoctor),
    path('deletedoctor/<id>',views.deletedoctor),
    path('addspecialties',views.addspecialties),
    path('listspecialties',views.listspecialties),
    path('aboutspecialties/<id>',views.aboutspecialties),
    path('aboutspecialties/updatespecialties/<id>',views.updatespecialties),
    path('addabouthospital',views.addabouthospital),
    path('listabouthospital',views.listabouthospital),
    path('addaddresshospital',views.addaddresshospital),
    path('contactus',views.contactus),
    path('contactusmessages',views.contactusmessages),
    path('addtreatments',views.addtreatments),
    path('listtreatments',views.listtreatments),
    path('updatetreatments/<id>',views.updatetreatments),
    path('deletetreatments/<id>',views.deletetreatments),
    path('addabouthospitalinfo',views.addabouthospitalinfo),
    path('updateabouthospitalinfo',views.updateabouthospitalinfo),
    path('makeappointment',views.makeappointment),
    path('viewappointment',views.viewappointment),
    path('appointmenthistory',views.appointmenthistory),

    

    
    
]

