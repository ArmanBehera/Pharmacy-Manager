from django.urls import path

import administrator.views
import doctor.views
from . import views


urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('getAppointmentDetail/', doctor.views.GetAppointmentDetail.as_view(), name='getAppointmentDetail'),
    path('getMedicines/', administrator.views.GetMedicines.as_view(), name='getMedicines'),
    path('getUniqueMedicines/', administrator.views.GetUniqueMedicines.as_view(), name="getUniqueMedicines"),
    path('addMedicines/', administrator.views.AddMedicines.as_view(), name='addMedicines'),
    path('addMedicineStock/', administrator.views.AddMedicineStock.as_view(), name='addMedicineStock'),
    path('deleteMedicines/', administrator.views.DeleteMedicines.as_view(), name='deleteMedicines'),
    path('getLabTests/', administrator.views.GetLabTests.as_view(), name='getLabTests'),
    path('getLabTestsDetailsForID/', doctor.views.GetLabTestsDetailsForID.as_view(), name='getLabTestsDetailsForID'),
    path('addLabTests/', administrator.views.AddLabTests.as_view(), name='addLabTests'),
    path('editLabTests/', administrator.views.EditLabTests.as_view(), name='editLabTests'),
    path('deleteLabTests/', administrator.views.DeleteLabTests.as_view(), name='deleteLabTests'),
    path('getDoctors/', views.GetDoctors.as_view(), name='getDoctors'),
    path('getCompletedPrescriptions/', doctor.views.GetCompletedPrescriptions.as_view(), name='getCompletedPrescriptions'),
    path('updateLabTests/', views.UpdateLabTests.as_view(), name='updateLabTests'),
    path('updatePrescription/', doctor.views.UpdatePrescription.as_view(), name='updatePrescription')
]