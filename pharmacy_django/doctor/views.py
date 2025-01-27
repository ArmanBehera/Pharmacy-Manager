from django.shortcuts import render
from rest_framework import views, response, status, permissions, exceptions
from administrator.models import User
from .models import DoctorUser, SpecializationAvailable, PatientUser, Appointment
from .serializers import DoctorSerializer, SpecializationSerializer, PatientSerializer, AppointmentSerializer
from administrator.serializers import UserSerializer
from administrator import authentication
import jwt
from django.conf import settings
from datetime import datetime, date

class SignIn(views.APIView):
    '''
        API view for doctor signin
    '''
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        '''
        Only post methods are allowed for this endpoint.
        The data posted is stored in User and DoctorUser model.
        '''
        
        serializer = DoctorSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorAPI(views.APIView):
    '''
        This viewpoint can only be used if the user is authenticated.
        This API does not do anything as of yet, just an example of how a view can be set which is only accessible to user who are authenticated.
    '''
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        user = request.user
        
        serializer = UserSerializer(user)
        
        return response.Response(serializer.data)
        

class PatientAPI(views.APIView):
    '''
        This viewpoint can only be used if the user is authenticated and the user is a doctor.
        This API also does not do anything as of yet, just an example for an API with doctor and authenticated requirements.
    '''
    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        pass


class GetPatientsForDoctor(views.APIView):

    '''
        Post method gets the patients that are scheduled for a particular doctor's appointment
    '''

    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        doctor_id = request.data['doctor_id']

        doctor = DoctorUser.objects.get(id=doctor_id)
        today = date.today()
        appointments = Appointment.objects.filter(doctor=doctor, status='Scheduled', date__gte=today).order_by('date', 'token_assigned')

        resp = []

        for appointment in appointments:
            serializer = AppointmentSerializer(appointment)

            resp.append(serializer.data)
        
        return response.Response(resp)


class Logout(views.APIView):
    '''
        Logout view can only be accessed by authenticated users
    '''
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        resp = response.Response()
        # resp.delete_cookie("jwt")
        
        resp.data = {"message": "Successfully logged out user."}
        
        return resp
        