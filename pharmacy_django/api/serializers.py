from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from doctor.models import DoctorUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes JWT's default serializer to include more information about the user.
    """

    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token['role'] = user.role
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Check if the user is verified
        if not self.user.is_verified:
            raise AuthenticationFailed('User is not verified. Contact Admin.')

        # Add user_id based on role
        if self.user.role != 'Doctor':
            data['user_id'] = self.user.id
        else:
            try:
                doctor_user = DoctorUser.objects.get(user=self.user)
                data['user_id'] = doctor_user.id
            except DoctorUser.DoesNotExist:
                raise AuthenticationFailed('Associated doctor record not found.')

        return data
