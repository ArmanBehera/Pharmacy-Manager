from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('getPatients/', views.GetPatientsForDoctor.as_view(), name='getPatients'),
    path('getAppointmentDetail/', views.GetAppointmentDetail.as_view(), name='getAppointmentDetail'),
    path('getMedicines/', views.GetMedicines.as_view(), name='getMedicines'),
    path('getLabTests/', views.GetLabTests.as_view(), name='getLabtests'),
    path('addPrescription/', views.AddPrescription.as_view(), name='addPrescription')
]
