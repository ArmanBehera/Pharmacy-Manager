from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('doctor/', views.DoctorAPI.as_view(), name='doctor'),
    path('getPatients/', views.GetPatientsForDoctor.as_view(), name='getPatients'),
]
