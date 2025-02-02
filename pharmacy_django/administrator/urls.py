from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('editProfile/', views.EditProfile.as_view(), name='editProfile'),
    path('verifyEmployees/', views.VerifyEmployees.as_view(), name='verifyEmployees'),
    path('getEmployees/', views.GetEmployees.as_view(), name='getEmployees'),
    path('deleteEmployees/', views.DeleteEmployees.as_view(), name='deleteEmployees'),
    path('getMedicines/', views.GetMedicines.as_view(), name='getMedicines'),
    path('getUniqueMedicines/', views.GetUniqueMedicines.as_view(), name="getUniqueMedicines"),
    path('addMedicines/', views.AddMedicines.as_view(), name='addMedicines'),
    path('addMedicineStock/', views.AddMedicineStock.as_view(), name='addMedicineStock'),
    path('deleteMedicines/', views.DeleteMedicines.as_view(), name='deleteMedicines'),
    path('getSpecializations/', views.GetSpecializationAvailable.as_view(), name='getSpecializations'),
    path('addSpecializations/', views.AddSpecializationAvailable.as_view(), name='addSpecializations'),
    path('editSpecializations/', views.EditSpecializationAvailable.as_view(), name='editSpecializations'),
    path('deleteSpecializations/', views.DeleteSpecializationAvailable.as_view(), name='deleteSpecializations'),
    path('getLabTests/', views.GetLabTests.as_view(), name='getLabTests'),
    path('addLabTests/', views.AddLabTests.as_view(), name='addLabTests'),
    path('editLabTests/', views.EditLabTests.as_view(), name='editLabTests'),
    path('deleteLabTests/', views.DeleteLabTests.as_view(), name='deleteLabTests'),
]