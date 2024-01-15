""

from django.urls import path,include
from CentralizedPatientApp import views
urlpatterns = [
    path('userindexpage',views.userindexpage),
    path('adduserinfo',views.adduserinfo),
    path('index/<id>',views.index),
    path('listabouthospital/<id>',views.listabouthospital),

    
    
    
]

""