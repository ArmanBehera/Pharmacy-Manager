from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('editProfile/', views.EditProfile.as_view(), name='editProfile'),
    path('verifyEmployees/', views.VerifyEmployees.as_view(), name='verifyEmployees'),
    path('viewEmployees/', views.ViewEmployees.as_view(), name='viewEmployees'),
    path('viewMedicines/', views.ViewMedicines.as_view(), name='viewMedicines'),
    path('addMedicines/', views.AddMedicines.as_view(), name="addMedicines"),
    path('specializations/', views.SpecializationAvailableView.as_view(), name="specializations"),
    path('addLabTest/', views.AddLabTest.as_view(), name='addLabTest'),
    path('viewLabTests/', views.ViewLabTests.as_view(), name='viewLabTests'),
    
]