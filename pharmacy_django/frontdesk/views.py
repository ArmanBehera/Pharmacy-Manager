from django.shortcuts import render
from rest_framework import views, response, status, permissions, exceptions
from administrator.serializers import UserSerializer
from administrator import authentication
from administrator.models import User
from doctor.models import DoctorUser, Appointment, PatientUser
from doctor.serializers import AppointmentSerializer, PatientSerializer
from datetime import datetime, date

class SignIn(views.APIView):
    '''
        API view for frontdesk signin
    '''
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        '''
        Only post methods are allowed for this endpoint.
        The data posted is stored in User model.
        '''
        
        if request.data['role'] != 'FrontDesk':
            return response.Response('Failed to create frontdesk user. Role should be assigned front desk.')

        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPatients(views.APIView):
    '''
        Post method is used to return all patients or ones match a particular filter
    '''
    #authentication_classes  = (authentication.CustomFrontDeskAuthentication, )
    #permission_classes = (permissions.IsAuthenticated, )

    # Filters that can be used: First Name, Last Name, Gender
    def post(self, request):
        
        patients = PatientUser.objects.filter(first_name__icontains=request.data['first_name'], last_name__icontains=request.data['last_name'], gender__icontains=request.data['gender'])

        resp = []

        for patient in patients:
            
            last_appointment = Appointment.objects.filter(patient=patient).order_by('-date').first()
            serializer = AppointmentSerializer(last_appointment)

            date = last_appointment.date
            date = date.strftime("%d-%m-%Y") 

            resp.append({'first_name': serializer.data['patient']['first_name'],'last_name': serializer.data['patient']['last_name'], 'gender': serializer.data['patient']['gender'], 'token_assigned': serializer.data['token_assigned'], 'appointment_date': datetime.strptime(serializer.data['date'], "%Y-%m-%d").strftime("%d-%m-%Y"), 'age': serializer.data['patient']['age']})

        return response.Response(resp)


class GetPatientsForDoctor(views.APIView):

    '''
        Post method gets the patients that are scheduled for a particular doctor's appointment
    '''

    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        doctor_id = request.data['doctor_id']

        doctor = DoctorUser.objects.get(id=doctor_id)
        today = date.today()
        appointments = Appointment.objects.filter(doctor=doctor, status='Scheduled', date__gte=today).order_by('date', 'token_assigned')

        resp = []

        for appointment in appointments:
            serializer = AppointmentSerializer(appointment)

            resp.append({'first_name': serializer.data['patient']['first_name'],'last_name': serializer.data['patient']['last_name'], 'gender': serializer.data['gender'], 'token_assigned': serializer.data['token_assigned'], 'appointment_date': datetime.strptime(serializer.data['date'], "%Y-%m-%d").strftime("%d-%m-%Y")})
        
        return response.Response(resp)


class GetDoctors(views.APIView):
    '''
        Get view is used to retun all the doctors
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        
        doctors = DoctorUser.objects.all()

        resp = []

        for doctor in doctors:
            doctor_data = {}

            doctor_data['id'] = doctor.id
            doctor_data['name'] = f'{doctor.user.first_name} {doctor.user.last_name}'
            doctor_data['specialization'] = str(doctor.specialization)

            resp.append(doctor_data)

        return response.Response(resp)


class AddPatient(views.APIView):
    '''
        Post View is used to add the preliminary details of the patient
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        # To add to the request: token_number: figure out the logic for that
        try:
            last_appointment_token = Appointment.objects.filter(doctor=request.data['doctor'], date=request.data['date']).order_by('-token_assigned').first().token_assigned
        except Exception:
            last_appointment_token = 0

        # The doctor's id is replaced with the actual doctor object as it would otherwise turn itself into its __str__ format.
        doctor = request.data['doctor']
        try:
            doctor = DoctorUser.objects.get(id=doctor)
        except Exception as e:
            raise response.Response(f'Failed to get the doctor user.')

        serializer = AppointmentSerializer(data={**request.data, 'token_assigned': last_appointment_token + 1, doctor: doctor})

        if serializer.is_valid():

            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
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
        