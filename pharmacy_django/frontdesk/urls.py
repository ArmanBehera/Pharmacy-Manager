from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('addNewPatient/', views.AddNewPatient.as_view(), name='addPatient'),
    path('addExistingPatient/', views.AddExistingPatient.as_view(), name='addExistingPatient'),
    path('getPatients/', views.GetPatients.as_view(), name='getPatients'),
    path('getDoctors/', views.GetDoctors.as_view(), name='getDoctors'),
    path('getPatientsForDoctor/', views.GetPatientsForDoctor.as_view(), name='getPatientsForDoctor'),
    path('cancelAppointment/', views.CancelAppointment.as_view(), name='cancelAppointment'),
    path('noShowUpdate/', views.NoShowUpdate.as_view(), name='noShowUpdate'),
    path('rebookAppointment/', views.RebookAppointment.as_view(), name='rebookAppointment'),
    path('getPreviousAppointments/', views.GetPreviousAppointments.as_view(), name='getPreviousAppointments')
]
