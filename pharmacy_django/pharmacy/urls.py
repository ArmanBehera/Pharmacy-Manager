from django.urls import path

import administrator.views
from . import views


urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('getMedicines/', administrator.views.GetMedicines.as_view(), name='getMedicines'),
    path('getUniqueMedicines/', administrator.views.GetUniqueMedicines.as_view(), name="getUniqueMedicines"),
    path('addMedicines/', administrator.views.AddMedicines.as_view(), name='addMedicines'),
    path('addMedicineStock/', administrator.views.AddMedicineStock.as_view(), name='addMedicineStock'),
    path('deleteMedicines/', administrator.views.DeleteMedicines.as_view(), name='deleteMedicines'),
    path('getLabTests/', administrator.views.GetLabTests.as_view(), name='getLabTests'),
    path('addLabTests/', administrator.views.AddLabTests.as_view(), name='addLabTests'),
    path('editLabTests/', administrator.views.EditLabTests.as_view(), name='editLabTests'),
    path('deleteLabTests/', administrator.views.DeleteLabTests.as_view(), name='deleteLabTests'),
]