from django.conf import settings
from rest_framework import authentication, exceptions
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User

class CustomUserAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        
        JWT_authenticator = JWTAuthentication()
        
        # Checks the request for validity
        try:
            response = JWT_authenticator.authenticate(request)
        
        except exceptions.AuthenticationFailed:
            return None
        
        if response is not None:
            # unpacking
            user, token = response
        else:
            return None
        
        return (user, None)
    


class CustomAdminAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        
        """
            Authenticate the user using a custom admin authentication logic.
        """
        JWT_authenticator = JWTAuthentication()

        try:
            # Attempt to authenticate using the JWT authenticator.
            response = JWT_authenticator.authenticate(request)
        except exceptions.AuthenticationFailed:
            # If the token is invalid, gracefully return None (no authentication).
            return None

        if response is not None:
            # Unpack the response if authentication is successful.
            user, token = response
        else:
            # No token provided; allow unauthenticated access if permission allows it.
            return None

        # Perform additional checks for admin privileges.
        if user.role != 'Admin' or not user.is_superuser:
            raise exceptions.PermissionDenied("Unauthorized access.")

        # Return the authenticated user and None for token (custom behavior).
        return (user, None)
    

class CustomDoctorAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        
        JWT_authenticator = JWTAuthentication()

        try: 
            response = JWT_authenticator.authenticate(request)

        except exceptions.AuthenticationFailed:
            return None
        
        
        if response is not None:
            # unpacking
            user, token = response
        else:
            return None
        
        if user.role != 'Doctor':
            raise exceptions.PermissionDenied("Unauthorized.")
        
        return (user, None)
    

class CustomPharmacyAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        
        JWT_authenticator = JWTAuthentication()

        try: 
            response = JWT_authenticator.authenticate(request)

        except exceptions.AuthenticationFailed:
            return None
        
        
        if response is not None:
            # unpacking
            user, token = response
        else:
            return None
        
        if user.role != 'Pharmacy':
            raise exceptions.PermissionDenied("Unauthorized.")
        
        return (user, None)
    
    
class CustomFrontDeskAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        
        JWT_authenticator = JWTAuthentication()

        try: 
            response = JWT_authenticator.authenticate(request)

        except exceptions.AuthenticationFailed:
            return None
        
        
        if response is not None:
            # unpacking
            user, token = response
        else:
            return None
        
        if user.role != 'FrontDesk':
            raise exceptions.PermissionDenied("Unauthorized.")
        
        return (user, None)
