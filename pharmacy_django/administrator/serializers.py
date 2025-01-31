from rest_framework import serializers, exceptions

from .models import User

class UserSerializer(serializers.ModelSerializer):
    '''
        Serializer for base user model
    '''
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        '''
            Meta data for the base user model. Contains all fields and overrides the optional ones.
        '''
        model = User
        fields = '__all__' # Uses all the fields defined in the model User
    
    # Had to override the default implementation because functionality was conflicting with password check
    def create(self, validated_data):
        user_data = validated_data
        # doctor_data = validated_data.pop('user')
            
        user = User.objects.create_user(**user_data)
        
        return user
    
         
    def validate_role(self, value):
        if value not in ['Administrator', 'Doctor', 'FrontDesk', 'Pharmacy']:
            raise exceptions.ValidationError(detail="Please enter a valid value for role.")
        
        return value
        
    
    def validate_gender(self, value):
        if value not in ['Male', 'Female', 'Other']:
            raise exceptions.ValidationError(detail="Gender of the user can only have three values: 'Male', 'Female' or 'Other'")
        return value


    def update(self, instance, validated_data):
        '''
            Fields that cannot be updated: first_name, last_name, is_superuser, is_staff, is_verified
        '''
        instance.username = validated_data.get('username', instance.username)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.primary_phone_number = validated_data.get('primary_phone_number', instance.primary_phone_number)
        instance.role = validated_data.get('role', instance.role)
        instance.email = validated_data.get('email', instance.email)
        instance.secondary_phone_number = validated_data.get('secondary_phone_number', instance.secondary_phone_number)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        instance.save()
        return instance