from django.contrib import admin
from .models import SpecializationAvailable, DoctorUser, PatientUser, Appointment

admin.site.register(SpecializationAvailable)
admin.site.register(DoctorUser)
admin.site.register(PatientUser)
admin.site.register(Appointment)