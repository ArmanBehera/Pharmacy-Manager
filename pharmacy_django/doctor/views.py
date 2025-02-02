from django.shortcuts import render
from rest_framework import views, response, status, permissions, exceptions
from administrator.models import User
from .models import DoctorUser, SpecializationAvailable, PatientUser, Appointment, PrescribedMedicine, PrescribedLabTest
from .serializers import DoctorSerializer, AppointmentSerializer, PrescriptionSerializer, PrescribedMedicinesSerializer, PrescribedLabTestsSerializer
from administrator.serializers import UserSerializer
from administrator import authentication
import jwt
from django.conf import settings
from datetime import datetime, date
from pharmacy.models import Medicines, LabTests
from pharmacy.serializers import MedicinesSerializer, LabTestsSerializer

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

        doctor = DoctorUser.objects.get(id=doctor_id)
        today = date.today()
        appointments = Appointment.objects.filter(doctor=doctor, status='Scheduled', date__gte=today).order_by('date', 'token_assigned')
        
        return response.Response(AppointmentSerializer(appointments, many=True).data)


class GetAppointmentDetail(views.APIView):
    '''
        On a successful post request, gets the appointment details for the id in the request
    '''

    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        appointment_id = request.data['id']

        appointment = Appointment.objects.get(id=appointment_id)

        return response.Response(AppointmentSerializer(appointment).data)


class GetMedicines(views.APIView):
    '''
        On a successful get request, returns all the medicines available
    '''
    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        medicines = Medicines.objects.all()

        return response.Response(MedicinesSerializer(medicines, many=True).data)


class GetLabTests(views.APIView):
    '''
        On a successful get request, returns all the lab tests available
    '''
    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        lab_tests = LabTests.objects.all()

        return response.Response(LabTestsSerializer(lab_tests, many=True).data)


class AddPrescription(views.APIView):
    '''
        On a successful post request, adds a prescription to an appointment
    '''
    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        appointment_id = request.data['appointment']
        appointment = Appointment.objects.get(id=appointment_id)

        if appointment.status == 'Scheduled':
            appointment.status = 'Completed'
            appointment.save()
        elif appointment.status == 'Completed':
            return response.Response('Cannot rewrite prescription. Please book another appointment.', status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response('Appointment is cancelled. Please rebook appointment in the frontdesk.', status=status.HTTP_400_BAD_REQUEST)

        serializer = PrescriptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPrescribedMedicines(views.APIView):
    '''
        On a successsful post request, enables to add a prescribed medicine
    '''

    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        serializer = PrescribedMedicinesSerializer(data=request.data)

        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPrescribedLabTests(views.APIView):
    '''
        On a successsful post request, enables to add a prescribed lab test
    '''

    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = PrescribedLabTestsSerializer(data=request.data)

        if serializer.is_valid():
            return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
