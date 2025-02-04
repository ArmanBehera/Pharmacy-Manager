from django.contrib import admin
from .models import SpecializationAvailable, DoctorUser, PatientUser, Appointment, Prescription, PrescribedLabTest, PrescribedMedicine

admin.site.register(SpecializationAvailable)
admin.site.register(DoctorUser)
admin.site.register(PatientUser)
admin.site.register(Appointment)
admin.site.register(PrescribedMedicine)
admin.site.register(PrescribedLabTest)
admin.site.register(Prescription)