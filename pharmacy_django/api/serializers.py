from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
        Customizes JWT's default serializer to include more information about the user
    '''

    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)

        token['role'] = user.role
        token['is_superuser'] = user.is_superuser

        if user.is_verified == False:
            return AuthenticationFailed('User is not verified. Contact Admin.')

        return token