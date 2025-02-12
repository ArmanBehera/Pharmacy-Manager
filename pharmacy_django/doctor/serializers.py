from rest_framework import serializers, exceptions

from .models import DoctorUser, PatientUser, SpecializationAvailable, Appointment, Prescription, PrescribedMedicine, PrescribedLabTest
from administrator.models import User
from pharmacy.models import Medicines, LabTests

from administrator.serializers import UserSerializer
from pharmacy.serializers import MedicinesSerializer, LabTestsSerializer

from doctor.models import UnlistedPrescribedMedicines, UnlistedPrescribedLabTests
  
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
        
    def validate_gender(self, value):
        if value not in ['Male', 'Female', 'Other']:
            raise serializers.ValidationError(detail="Gender of the user can only have three values: 'Male', 'Female' or 'Other'")
        return value



class UnlistedMedicinesSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnlistedPrescribedMedicines
        fields = '__all__'
    

class UnlistedLabTestsSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnlistedPrescribedLabTests
        fields = '__all__'

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
        except Exception as e:
            raise serializers.ValidationError(e)
        
        validated_data['patient'] = patient

        appointment = Appointment.objects.create(**validated_data)

        return appointment

class PrescribedMedicinesSerializer(serializers.ModelSerializer):

    class Meta: 
        model = PrescribedMedicine
        fields = '__all__'



class PrescribedLabTestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrescribedLabTest
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):

    lab_tests = PrescribedLabTestsSerializer(many=True, required=False)
    medicines = PrescribedMedicinesSerializer(many=True, required=False)
    unlisted_lab_tests = UnlistedLabTestsSerializer(many=True, required=False)
    unlisted_medicines = UnlistedMedicinesSerializer(many=True, required=False)

    class Meta:
        model =  Prescription
        exclude = ['created_at']

    def create(self, validated_data):
        prescribed_medicines_data = validated_data.pop('medicines', [])
        prescribed_lab_tests_data = validated_data.pop('lab_tests', [])
        unlisted_medicines_data = validated_data.pop('unlisted_medicines', [])
        unlisted_lab_tests_data = validated_data.pop('unlisted_lab_tests', [])

        try:
            prescription = Prescription.objects.create(**validated_data)

            if prescribed_medicines_data:
                prescribed_medicines = [PrescribedMedicine.objects.create(**prescribed_medicine_data) for prescribed_medicine_data in prescribed_medicines_data]
                prescription.medicines.set(prescribed_medicines)
            
            if prescribed_lab_tests_data:
                prescribed_lab_test = [PrescribedLabTest.objects.create(**prescribed_lab_test_data) for prescribed_lab_test_data in prescribed_lab_tests_data]
                prescription.lab_tests.set(prescribed_lab_test)

            if unlisted_medicines_data:
                unlisted_medicines = [UnlistedPrescribedMedicines.objects.create(**unlisted_medicine_data) for unlisted_medicine_data in unlisted_medicines_data]
                prescription.unlisted_medicines.set(unlisted_medicines)

            if unlisted_lab_tests_data:
                unlisted_lab_tests = [UnlistedPrescribedLabTests.objects.create(**unlisted_lab_test_data) for unlisted_lab_test_data in unlisted_lab_tests_data]
                prescription.unlisted_lab_tests.set(unlisted_lab_tests)

            return prescription
        
        except Exception as e:
            prescription.delete()  # Rollback changes
            raise serializers.ValidationError({'error': f'Failed to create Prescription. {e}'})
