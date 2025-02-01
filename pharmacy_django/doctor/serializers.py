from rest_framework import serializers, exceptions

from .models import DoctorUser, PatientUser, SpecializationAvailable, Appointment, Prescription, PrescribedMedicine, PrescribedLabTest
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
        
    def validate_gender(self, value):
        if value not in ['Male', 'Female', 'Other']:
            raise serializers.ValidationError(detail="Gender of the user can only have three values: 'Male', 'Female' or 'Other'")
        return value
    

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
'''
class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = serializers.ListField(child=serializers.DictField(), required=False)
    lab_tests = serializers.PrimaryKeyRelatedField(queryset=PrescribedLabTest.objects.all(), many=True, required=False)
    unlisted_medicines = UnlistedMedicinesSerializer(required=False, many=True)
    unlisted_lab_tests = UnlistedLabTestsSerializer(required=False, many=True) 

    class Meta:
        model = Prescription
        fields = '__all__'

    def create(self, validated_data):
        try:
            # 🔹 Extract appointment ID
            appointment = validated_data.pop('appointment', None)
            if not appointment:
                raise serializers.ValidationError({'appointment': 'This field is required.'})
            
            # 🔹 Extract related fields
            medicines_data = validated_data.pop('medicines', [])
            lab_tests_data = validated_data.pop('lab_tests', [])
            unlisted_medicines_data = validated_data.pop('unlisted_medicines', [])
            unlisted_lab_tests_data = validated_data.pop('unlisted_lab_tests', [])

            # 🔹 Create Prescription instance
            prescription = Prescription.objects.create(appointment=appointment, **validated_data)

            # 🔹 Handle Medicines
            prescribed_medicines = []
            for medicine_data in medicines_data:
                medicine_id = medicine_data.get("id")
                if not medicine_id:
                    raise serializers.ValidationError({'medicines': 'Each medicine must have an ID.'})
                
                medicine_instance = Medicines.objects.get(id=medicine_id)  
                
                prescribed_medicine = PrescribedMedicine.objects.create(
                    medicine=medicine_instance,
                    frequency=medicine_data.get("frequency"),
                    duration_value=medicine_data.get("duration_value"),
                    duration_unit=medicine_data.get("duration_unit")
                )
                prescribed_medicines.append(prescribed_medicine)

            if prescribed_medicines:
                prescription.medicines.set(prescribed_medicines)

            # 🔹 Handle Lab Tests (FIXED)
            if lab_tests_data:
                lab_tests_instances = PrescribedLabTest.objects.filter(id__in=lab_tests_data)  # Convert IDs to objects
                prescription.lab_tests.set(lab_tests_instances)

            # 🔹 Handle Unlisted Medicines
            unlisted_medicines = [UnlistedMedicine.objects.create(**um_data) for um_data in unlisted_medicines_data]
            if unlisted_medicines:
                prescription.unlisted_medicines.set(unlisted_medicines)

            # 🔹 Handle Unlisted Lab Tests
            unlisted_lab_tests = [UnlistedLabTest.objects.create(**ult_data) for ult_data in unlisted_lab_tests_data]
            if unlisted_lab_tests:
                prescription.unlisted_lab_tests.set(unlisted_lab_tests)

            return prescription

        except Exception as e:
            print("Error:", str(e))  # Debugging log
            prescription.delete()  # Rollback changes
            raise serializers.ValidationError({'error': 'Failed to create Prescription. See logs for details.'})
'''


class PrescribedMedicinesSerializer(serializers.ModelSerializer):

    class Meta: 
        model = PrescribedMedicine
        fields = '__all__'



class PrescribedLabTestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrescribedLabTest
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):

    # appointment is created directly using primary key
    lab_tests = PrescribedLabTestsSerializer(many=True, required=False)
    medicines = PrescribedMedicinesSerializer(many=True, required=False)
    # medicines = serializers.PrimaryKeyRelatedField(queryset=PrescribedMedicine.objects.all(), many=True, required=False)
    # lab_tests = serializers.PrimaryKeyRelatedField(queryset=PrescribedLabTest.objects.all(), many=True, required=False)
    unlisted_lab_tests = UnlistedLabTestsSerializer(many=True, required=False)
    unlisted_medicines = UnlistedMedicinesSerializer(many=True, required=False)

    class Meta:
        model =  Prescription
        fields = '__all__'

    def create(self, validated_data):
        prescribed_medicines_data = validated_data.pop('medicines', [])
        prescribed_lab_tests_data = validated_data.pop('lab_tests', [])
        unlisted_medicines_data = validated_data.pop('unlisted_medicines', [])
        unlisted_lab_tests_data = validated_data.pop('unlisted_lab_tests', [])

        prescription = Prescription.objects.create(**validated_data)

        if prescribed_medicines_data:
            prescribed_medicines = [PrescribedMedicine.objects.create(**prescribed_medicine_data) for prescribed_medicine_data in prescribed_medicines_data]
            prescription.medicines.set(prescribed_medicines)
        
        if prescribed_lab_tests_data:
            prescribed_lab_test = [PrescribedLabTest.objects.create(**prescribed_lab_test_data) for prescribed_lab_test_data in prescribed_lab_tests_data]
            prescription.lab_tests.set(prescribed_lab_test)

        if unlisted_medicines_data:
            unlisted_medicines = [UnlistedMedicine.objects.create(**unlisted_medicine_data) for unlisted_medicine_data in unlisted_medicines_data]
            prescription.unlisted_medicines.set(unlisted_medicines)

        if unlisted_lab_tests_data:
            unlisted_lab_tests = [UnlistedLabTest.objects.create(**unlisted_lab_test_data) for unlisted_lab_test_data in unlisted_lab_tests_data]
            prescription.unlisted_lab_tests.set(unlisted_lab_tests)

        return prescription
        '''
        except Exception as e:
            prescription.delete()  # Rollback changes
            raise serializers.ValidationError({'error': f'Failed to create Prescription. {e}'})
        '''
