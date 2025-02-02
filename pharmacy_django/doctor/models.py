from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from administrator.models import User
from django.utils import timezone
from pharmacy.models import Medicines, LabTests, UnlistedPrescribedMedicines, UnlistedPrescribedLabTests


class SpecializationAvailable(models.Model):
    '''
        Stores all the specializations available
    '''
    
    specialization = models.CharField(max_length = 128, blank=False)

    def __str__(self):
        return f"{self.specialization}"
    

class DoctorUser(models.Model):
    user = models.OneToOneField(User, verbose_name="Doctor User Details", on_delete=models.PROTECT, related_name="doctor")
    consultation_fee = models.IntegerField(validators=[MinValueValidator(0)], blank=False, default=None)
    experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], blank=True, null=True, default=None)
    registration_number = models.CharField(unique=True, blank=False, default=None, max_length=50)
    specialization = models.ForeignKey(SpecializationAvailable, verbose_name="Specialization field for this doctor", on_delete=models.PROTECT, related_name="doctor", blank=False, null=True, default=None)
    # availability = // To think of a way to represent availability

    def __str__(self):
        return f"Name: {self.user.first_name} {self.user.last_name}. Specialization: {self.specialization}"


class PatientUser(models.Model):
    
    first_name = models.CharField(max_length=100, blank=False, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], blank=False, null=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, blank=False, null=True)
    
    primary_phone_number = models.CharField(max_length=15, blank=False, null=True)
    secondary_phone_number = models.CharField(max_length=15, blank=True, null=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient Name: {self.first_name} {self.last_name}"
    
    
class Appointment(models.Model):
    
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
    ]
    
    doctor = models.ForeignKey(DoctorUser, verbose_name="Doctor", on_delete=models.PROTECT, related_name='appointments')
    patient = models.ForeignKey(PatientUser, verbose_name="Patient", on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(default=timezone.now, verbose_name="Appointment Date")
    token_assigned = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=True, verbose_name="Token Assigned")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled', verbose_name="Status")
    
    def __str__(self):
        return f"Appointment with Dr. {self.doctor} for {self.patient} on {self.date}. Token Number: {self.token_assigned}"


class PrescribedMedicine(models.Model):

    DURATION_UNIT_CHOICES = [
        ('Days', 'Days'),
        ('Months', 'Months')
    ]

    MEDICINES_STATUS_CHOICES = [
        ('Prescribed', 'Prescribed'),
        ('Dispensed', 'Dispensed'),
        ('Not Available', 'Not Available')
    ]

    medicine = models.ForeignKey(Medicines, verbose_name="Medicine Details", on_delete=models.CASCADE, related_name="prescribed_medicine")
    frequency = models.IntegerField(validators=[MinValueValidator(1)], help_text="Number of times the medicine should be taken per day")
    duration_value = models.FloatField(validators=[MinValueValidator(1)], help_text="Duration value based on the selected unit")
    duration_unit = models.CharField(max_length=6, choices=DURATION_UNIT_CHOICES, verbose_name="Duration Unit")
    status = models.CharField(max_length=13, choices=MEDICINES_STATUS_CHOICES, default='Prescribed', verbose_name="Medicine Status", blank=False, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(frequency__gte=1),
                name='check_valid_frequency'
            ),
            models.CheckConstraint(
                check=models.Q(duration_value__gte=1),
                name='check_valid_duration_value'
            ),
        ]

    def __str__(self):
        return f"{self.medicine.name} - {self.frequency}x per day, {self.duration_value} {self.get_duration_unit_display()}"
    

class PrescribedLabTest(models.Model):
    
    LAB_TESTS_STATUS_CHOICES = [
        ('Prescribed', 'Prescribed'),
        ('Sample Collected', 'Sample Collected'),
        ('Report Collected', 'Report Collected'),
        ('Patient Informed', 'Patient Informed')
    ]

    lab_test = models.ForeignKey(LabTests, verbose_name="Lab Test", on_delete=models.PROTECT, related_name="prescribed_lab_test")
    test_date = models.DateField(verbose_name="Test Date", blank=True, null=True)
    test_result = models.TextField(verbose_name="Test Result", blank=True, null=True)
    status = models.CharField(max_length=16, choices=LAB_TESTS_STATUS_CHOICES, default='Prescribed', verbose_name="Lab Test Status") 
    sample_tracking_code = models.CharField(max_length=255, blank=True, null=True)
    attachment = models.FileField(upload_to='lab_tests/', verbose_name="Test Report", blank=True, null=True)

    def __str__(self):
        return f"{self.lab_test} prescribed for {self.lab_test.name} on {self.test_date}. Status: {self.status}."


class Prescription(models.Model):

    appointment = models.OneToOneField(Appointment, verbose_name="Appointment Details", on_delete=models.CASCADE, related_name='prescription')
    medicines  = models.ManyToManyField(PrescribedMedicine, verbose_name="Prescribed Medicines", related_name='prescription', blank=True)
    unlisted_medicines = models.ManyToManyField(UnlistedPrescribedMedicines, verbose_name= "Prescribed Unlisted Medicines", related_name='prescription', blank=True)
    lab_tests = models.ManyToManyField(PrescribedLabTest, verbose_name="Prescribed Lab Tests", related_name='prescription', blank=True)
    unlisted_lab_tests = models.ManyToManyField(UnlistedPrescribedLabTests, verbose_name="Prescribed Unlisted Lab Tests", related_name='prescription', blank=True)
    additonal_information = models.TextField(verbose_name="Description", blank=True, null=True, help_text="Additional Information for the patient")

    def __str__(self):
        patient = self.appointment.patient
        return f"Prescription for {patient.first_name} {patient.last_name}."