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
    authentication_classes  = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    # Filters that can be used: First Name, Last Name, Gender
    def post(self, request):
        
        patients = PatientUser.objects.filter(first_name__icontains=request.data['first_name'], last_name__icontains=request.data['last_name'], gender__icontains=request.data['gender'])

        resp = []

        for patient in patients:
            
            last_appointment = Appointment.objects.filter(patient=patient).order_by('-date').first()
            serializer = AppointmentSerializer(last_appointment)

            date = last_appointment.date
            date = date.strftime("%d-%m-%Y") 

            resp.append({'id': serializer.data['patient']['id'], 'first_name': serializer.data['patient']['first_name'],'last_name': serializer.data['patient']['last_name'], 'gender': serializer.data['patient']['gender'], 'token_assigned': serializer.data['token_assigned'], 'appointment_date': datetime.strptime(serializer.data['date'], "%Y-%m-%d").strftime("%d-%m-%Y"), 'age': serializer.data['patient']['age']})

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
        
        return response.Response(AppointmentSerializer(appointments, many=True).data)


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


class AddNewPatient(views.APIView):
    '''
        Post View is used to add the preliminary details of the patient
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        # To add to the request: token_number: figure out the logic for that
        doctor_id = request.data['doctor_id']
        doctor = DoctorUser.objects.get(id=doctor_id)
        
        try:
            last_appointment_token = Appointment.objects.filter(doctor=doctor, date=request.data['date']).order_by('-token_assigned').first().token_assigned
        except Exception:
            last_appointment_token = 0

        doctor_id = request.data['doctor_id']

        serializer = AppointmentSerializer(data={**request.data, 'token_assigned': last_appointment_token + 1, 'doctor': doctor_id})

        if serializer.is_valid():

            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddExistingPatient(views.APIView):
    '''
        Post View is used to create an appointment for an existing patient
    '''
    #authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    #permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        patient_id = request.data['patient_id']
        patient = PatientUser.objects.get(id=patient_id)

        doctor_id = request.data['doctor_id']
        doctor = DoctorUser.objects.get(id=doctor_id)
    
        try:
            last_appointment_token = Appointment.objects.filter(doctor=doctor, date=request.data['date']).order_by('-token_assigned').first().token_assigned
        except AttributeError:
            last_appointment_token = 0

        try:
            # Try to parse the date into a valid format (e.g., YYYY-MM-DD)
            date = datetime.strptime(request.data['date'], '%Y-%m-%d').date()
        except ValueError:
            return response.Response('Unable to make an appointment.')

        appointment = Appointment.objects.create(patient=patient, doctor=doctor, date=date, token_assigned=last_appointment_token + 1, status=request.data['status'])
        appointment.save()

        return response.Response({ 'token': appointment.token_assigned })   


class NoShowUpdate(views.APIView):
    '''
        Post View is used to create an appointment for an existing patient
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        # Refreshing the statuses of the patient who did not show up
        today = datetime.now().date()
        scheduledAppointments = Appointment.objects.filter(status='Scheduled', date__lt=today)

        # Update their statuses
        scheduledAppointments.update(status='No Show')
        noShowAppointments = Appointment.objects.filter(status='No Show')

        serializer = AppointmentSerializer(noShowAppointments, many=True)

        return response.Response(serializer.data)


class CancelAppointment(views.APIView):
    '''
        On a successful post request, cancels the appointment of the patient with the given id.
    '''

    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        id = request.data['id']

        try:
            appointment = Appointment.objects.get(id=id)
            appointment.status = 'Cancelled'
            appointment.save()
        except:
            return response.Response('Failed to delete the appointment for the patient.', status=status.HTTP_400_BAD_REQUEST)

        return response.Response('Successful in deleting the appointment for the patient.', status=status.HTTP_200_OK)


class Logout(views.APIView):
    '''
        Logout view can only be accessed by authenticated users
    '''
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):

        resp = response.Response()
        
        resp.data = {"message": "Successfully logged out user."}
        
        return resp
        