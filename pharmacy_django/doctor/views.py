from django.shortcuts import render
from django.utils import timezone
from rest_framework import views, response, status, permissions, exceptions
from administrator.models import User
from .models import DoctorUser, SpecializationAvailable, PatientUser, Appointment, PrescribedMedicine, PrescribedLabTest, Prescription
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


class GetMedicinesDetailsForID(views.APIView):
    
    authentication_classes = (authentication.CombinedPharmacyAndDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        medicine = PrescribedMedicine.objects.get(id=request.data['id']).medicine

        return response.Response(MedicinesSerializer(medicine).data, status=status.HTTP_202_ACCEPTED)


class GetLabTestsDetailsForID(views.APIView):
    
    authentication_classes = (authentication.CombinedPharmacyAndDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        lab_test = PrescribedLabTest.objects.get(id=request.data['id']).lab_test

        return response.Response(LabTestsSerializer(lab_test).data, status=status.HTTP_202_ACCEPTED)



class GetAppointmentDetail(views.APIView):
    '''
        On a successful post request, gets the appointment details for the id in the request
    '''

    authentication_classes = (authentication.CombinedPharmacyAndDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        appointment_id = request.data['id']

        appointment = Appointment.objects.get(id=appointment_id)

        return response.Response(AppointmentSerializer(appointment).data)

class GetCompletedPrescriptions(views.APIView):
    '''
        In a get request, returns all the patients for whom medicines are to be given
    '''
    authentication_classes = (authentication.CombinedPharmacyAndDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        if request.data.get('doctor_id'):
            today = timezone.now().date()

            doctor_id = request.data['doctor_id']
            doctor = DoctorUser.objects.get(id=doctor_id)

            resp = []
            
            # Returns the medicines
            if request.data.get('code') == 1:
                prescriptions = Prescription.objects.filter(
                    medicines_fulfilled=False, appointment__doctor=doctor
                )

                for prescription in prescriptions:
                    appointment = prescription.appointment
                    resp.append({
                        'prescription_id': prescription.id,
                        'name': f'{appointment.patient.first_name} {appointment.patient.last_name}',
                        'created_at': prescription.created_at.time().strftime('%H:%M:%S')
                    })

            # Returns the lab tests
            elif request.data.get('code') == 2:
                prescriptions = Prescription.objects.filter(
                    lab_tests_completed=False, appointment__doctor=doctor
                )

                for prescription in prescriptions:
                    appointment = prescription.appointment
                    resp.append({
                        'prescription_id': prescription.id,
                        'name': f'{appointment.patient.first_name} {appointment.patient.last_name}',
                        'created_at': prescription.created_at.time().strftime('%H:%M:%S')
                    })

            return response.Response(resp, status=status.HTTP_202_ACCEPTED)
        
        # Returns the details of one prescription
        elif request.data.get('prescription_id'):  # Check if 'prescription_id' exists

            prescription = Prescription.objects.get(id=request.data['prescription_id'])

            return response.Response(PrescriptionSerializer(prescription).data)

        else:
            return response.Response('Incorrect data format.', status=status.HTTP_400_BAD_REQUEST)


class GetPrescriptionID(views.APIView):
    '''
        On a successful post request, returns the prescription id from the appointment id
            If no prescription is found, return None
    '''

    authentication_classes = (authentication.CustomDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        appointment_id = request.data['appointment_id']
        appointment = Appointment.objects.get(id=appointment_id)

        # return response.Response(AppointmentSerializer(appointment).data)
        try:
            prescription = Prescription.objects.get(appointment=appointment)

            return response.Response(prescription.id, status=status.HTTP_202_ACCEPTED)
        except Prescription.DoesNotExist:
            return response.Response('Could not find prescription for this appointment id.', status=status.HTTP_400_BAD_REQUEST)



class UpdatePrescription(views.APIView):
    '''
        On a successful post request, partially update the prescription    
    '''
    authentication_classes = (authentication.CombinedPharmacyAndDoctorAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        data = request.data.copy()  # Create a mutable copy of request.data
        prescription_id = data.pop('id', None)  # Remove 'id' safely

        if not prescription_id:
            return response.Response({'error': 'Prescription ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            prescription = Prescription.objects.get(id=prescription_id)
        except Prescription.DoesNotExist:
            return response.Response({'error': 'Prescription not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PrescriptionSerializer(prescription, data=data, partial=True)  # Pass modified data

        if serializer.is_valid():
            serializer.save()
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
