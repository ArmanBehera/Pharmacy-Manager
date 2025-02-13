from django.conf import settings
from rest_framework import authentication, exceptions
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication


class CombinedPharmacyAndAdminAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        
        JWT_authenticator = JWTAuthentication()

        try:
            response = JWT_authenticator.authenticate(request)
        except exceptions.AuthenticationFailed:
            return None

        if response is not None:
            user, token = response
        else:
            return None

        # Perform additional checks for admin privileges.
        if user.role != 'Administrator' and user.role != 'Pharmacy':
            raise exceptions.PermissionDenied("Unauthorized access.")

        return (user, None)