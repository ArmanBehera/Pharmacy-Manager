from rest_framework import serializers

from .models import DoctorUser, PatientUser, SpecializationAvailable, Appointment, Prescription
from administrator.models import User
from pharmacy.models import Medicines, LabTests, UnlistedMedicine, UnlistedLabTest

from administrator.serializers import UserSerializer
from pharmacy.serializers import MedicinesSerializer, LabTestsSerializer, UnlistedMedicinesSerializer, UnlistedLabTestsSerializer
  
class SpecializationSerializer(serializers.ModelSerializer):
    '''
        Serializer for specialization serializer
    '''
    
    class Meta:
        model = SpecializationAvailable
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(many=False, required=True)

    class Meta:
        
        model = DoctorUser
        fields = '__all__'
        
    def create(self, validated_data):
        
        user_data = validated_data['user']
        specialization = validated_data['specialization']
        
        try: 
            user = User.objects.create_user(**user_data)
        except Exception:
            raise serializers.ValidationError("Failed to create user.")

        specialization = SpecializationAvailable.objects.get(id=specialization.id)
        validated_data['user'] = user
        validated_data['specialization'] = specialization

        try: 
            doctor = DoctorUser.objects.create(**validated_data)
            return doctor
        except Exception:
            user.delete()
            return serializers.ValidationError("Failed to create doctor user.")


    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user) # Make a user object

        if validated_data['user']:
            UserSerializer(instance.user, data=validated_data['user']) # Using the serializer will automatically update the instance and need not be reassigned.

        # The first parameter is the value assigned if the field is there in the data, otherwise it reverts back to the second parameter.
        instance.consultation_fee = validated_data.get('consultation_fee', instance.consultation_fee)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        instance.specialization = validated_data.get('specialization', instance.specialization)

        # Saves the updated instance
        instance.save()
        return instance
    
        
class PatientSerializer(serializers.ModelSerializer):
    '''
        There's no way to update a Patient object. Once created cannot be deleted or modified
    '''
    
    class Meta:
        
        model = PatientUser
        fields = '__all__'
        
    def create(self, validated_data):

        # If the below line shows an error, it's not
        patient = PatientUser.objects.create(**validated_data)
        
        return patient
    

class AppointmentSerializer(serializers.ModelSerializer):
    '''
        Serializer to book an appointment
    '''

    patient = PatientSerializer(required=True, many=False)

    class Meta: 

        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        
        patient_data = validated_data['patient']

        try:
            patient = PatientUser.objects.create(**patient_data)
        except Exception:
            raise serializers.ValidationError('Failed to make a new patient.')
        
        validated_data['patient'] = patient

        appointment = Appointment.objects.create(**validated_data)

        return appointment
    

class PrescriptionSerializer(serializers.ModelSerializer):

    # For the commmented out code, just need to provide the ids
    # appointment = AppointmentSerializer(required=True, many=False)
    # medicines = MedicinesSerializer(required=False, many=True)
    # labTests = LabTestsSerializer(required=False, many=True)
    unlistedMedicines = UnlistedMedicinesSerializer(required=False, many=True)
    unlistedLabTests = UnlistedLabTestsSerializer(required=False, many=True) 

    class Meta:

        model = Prescription
        fields = '__all__'

    def create(self, validated_data):
        # Extract the appointment ID and fetch the actual object
        appointment_data = validated_data.pop('appointment')
        appointment = Appointment.objects.get(id=appointment_data)
        
        # Extract related fields safely
        medicines_data = validated_data.pop('medicines', [])
        lab_tests_data = validated_data.pop('labTests', [])
        unlisted_medicines_data = validated_data.pop('unlistedMedicines', [])
        unlisted_lab_tests_data = validated_data.pop('unlistedLabTests', [])

        # Create the Prescription instance without M2M relationships
        prescription = Prescription.objects.create(appointment=appointment, **validated_data)

        # Assign Many-to-Many fields
        if medicines_data:
            medicines = Medicines.objects.filter(id__in=[m['id'] for m in medicines_data])
            prescription.medicines.set(medicines)

        if lab_tests_data:
            lab_tests = LabTests.objects.filter(id__in=[lt['id'] for lt in lab_tests_data])
            prescription.labtests.set(lab_tests)

        if unlisted_medicines_data:
            unlisted_medicines = UnlistedMedicine.objects.filter(id__in=[um['id'] for um in unlisted_medicines_data])
            prescription.unlistedMedicines.set(unlisted_medicines)

        if unlisted_lab_tests_data:
            unlisted_lab_tests = UnlistedLabTest.objects.filter(id__in=[ult['id'] for ult in unlisted_lab_tests_data])
            prescription.unlistedLabTests.set(unlisted_lab_tests)

        return prescription

