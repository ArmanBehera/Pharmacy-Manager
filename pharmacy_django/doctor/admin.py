from django.contrib import admin
from .models import SpecializationAvailable, DoctorUser, PatientUser, Appointment, Prescription

admin.site.register(SpecializationAvailable)
admin.site.register(DoctorUser)
admin.site.register(PatientUser)
admin.site.register(Appointment)
admin.site.register(Prescription)