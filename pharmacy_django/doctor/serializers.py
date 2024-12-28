from rest_framework import serializers

from .models import DoctorUser, PatientUser, SpecializationAvailable, Appointment
from administrator.models import User
from administrator.serializers import UserSerializer
  
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
        doctor_id = validated_data['doctor']

        try:
            patient = PatientUser.objects.create(**patient_data)
        except Exception:
            raise serializers.ValidationError('Failed to make a new patient.')
        
        try:
            doctor = DoctorUser.objects.get(id=doctor_id)
        except Exception:
            raise serializers.ValidationError('Failed to get the doctor user.')

        validated_data['patient'] = patient
        validated_data['doctor'] = doctor

        appointment = Appointment.objects.create(**validated_data)

        return appointment