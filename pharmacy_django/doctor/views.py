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


class GetPatientsForDoctor(views.APIView):

    '''
        Post method gets the patients that are scheduled for a particular doctor's appointment
    '''

    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        try:
            doctor_id = request.data['doctor_id']
        except:
            return response.Response('Failed to get doctor id.')

        # Refreshing the statuses of the patient who did not show up
        today = datetime.now().date()
        appointments = Appointment.objects.filter(status='Scheduled', date__lt=today)

        # Update their statuses
        appointments.update(status='No Show')  # Example: Mark as 'No Show'

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
