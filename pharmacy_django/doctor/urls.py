from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('getPatients/', views.GetPatientsForDoctor.as_view(), name='getPatients'),
    path('getAppointmentDetail/', views.GetAppointmentDetail.as_view(), name='getAppointmentDetail'),
    path('getMedicines/', views.GetMedicines.as_view(), name='getMedicines'),
    path('getLabTests/', views.GetLabTests.as_view(), name='getLabtests'),
    path('addPrescription/', views.AddPrescription.as_view(), name='addPrescription'),
    path('addPrescribedMedicines/', views.AddPrescribedMedicines.as_view(), name='addPrescribedMedicines'),
    path('addPrescribedLabTests/', views.AddPrescribedLabTests.as_view(), name='addPrescribedLabTests'),
    path('getAppointmentDetail/', views.GetAppointmentDetail.as_view(), name='getAppointmentDetail'),
    path('getLabTestsDetailsForID/', views.GetLabTestsDetailsForID.as_view(), name='getLabTestsDetailsForID'),
    path('getMedicinesDetailsForID/', views.GetMedicinesDetailsForID.as_view(), name='getMedicinesDetailsForID'),
    path('getCompletedPrescriptions/', views.GetCompletedPrescriptions.as_view(), name='getCompletedPrescriptions'),
    path('getPrescriptionID/', views.GetPrescriptionID.as_view(), name='getPrescriptionID'),
    path('updatePrescription/', views.UpdatePrescription.as_view(), name='updatePrescription')
]
