from rest_framework import views, response, status, permissions, exceptions
from administrator.serializers import UserSerializer
from administrator import authentication
from administrator.models import User
from doctor.models import DoctorUser, Appointment, PatientUser, Prescription
from doctor.serializers import AppointmentSerializer, PatientSerializer, DoctorSerializer, PrescriptionSerializer
from datetime import datetime, date
from django.db.models import Sum, F, Q
from django.core.exceptions import ObjectDoesNotExist

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
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
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
            try:
                last_appointment = Appointment.objects.filter(patient=patient).order_by('-date').first()
                serializer = AppointmentSerializer(last_appointment)

                date = last_appointment.date
                date = date.strftime("%d-%m-%Y")

                resp.append({'id': serializer.data['patient']['id'], 'first_name': serializer.data['patient']['first_name'],'last_name': serializer.data['patient']['last_name'], 'gender': serializer.data['patient']['gender'], 'token_assigned': serializer.data['token_assigned'], 'appointment_date': datetime.strptime(serializer.data['date'], "%Y-%m-%d").strftime("%d-%m-%Y"), 'age': serializer.data['patient']['age']})
            except: 
                continue
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
        
        doctors = DoctorUser.objects.filter(user__is_verified=True)

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
        doctor_id = request.data['doctor']
        doctor = DoctorUser.objects.get(id=doctor_id)
        
        try:
            last_appointment_token = Appointment.objects.filter(doctor=doctor, date=request.data['date']).order_by('-token_assigned').first().token_assigned
        except Exception:
            last_appointment_token = 0

        serializer = AppointmentSerializer(data={**request.data, 'token_assigned': last_appointment_token + 1 })

        if serializer.is_valid():

            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddExistingPatient(views.APIView):
    '''
        Post View is used to create an appointment for an existing patient
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        patient_id = request.data['patient_id']
        patient = PatientUser.objects.get(id=patient_id)

        doctor_id = request.data['doctor_id']

        print()
        print(doctor_id)
        print()

        if doctor_id == -1:
            previous_appointment_id = request.data['previous_appointment_id']
            previous_appointment = Appointment.objects.get(id=previous_appointment_id)
            doctor = previous_appointment.doctor
        else:
            previous_appointment = None
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

        appointment = Appointment.objects.create(patient=patient, doctor=doctor, date=date, token_assigned=last_appointment_token + 1, previous_appointment=previous_appointment, status=request.data['status'])
        appointment.save()

        return response.Response({ 'token': appointment.token_assigned })   


class NoShowUpdate(views.APIView):
    '''
        Post View is used to create an appointment for an existing patient
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        # Refreshing the statuses of the patient who did not show up
        today = datetime.now().date()
        scheduled_appointments = Appointment.objects.filter(status='Scheduled', date__lt=today)

        # Update their statuses
        scheduled_appointments.update(status='No Show')

        doctor_id = request.data['doctor_id']
        doctor = DoctorUser.objects.get(id=doctor_id)

        no_show_appointments = Appointment.objects.filter(status='No Show', doctor=doctor)
        
        return response.Response(AppointmentSerializer(no_show_appointments, many=True).data)


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


class RebookAppointment(views.APIView):

    '''
        On a successful request, changes the status of a 'no-show' appointment to a 'scheduled' appointment
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        id = request.data['id']
        date = request.data['date']

        try:
            appointment = Appointment.objects.get(id=id)
            doctor = appointment.doctor
        
            try:
                last_appointment_token = Appointment.objects.filter(doctor=doctor, date=request.data['date']).order_by('-token_assigned').first().token_assigned
            except AttributeError:
                last_appointment_token = 0

            
            serializer = AppointmentSerializer(appointment, {'status': 'Scheduled', 'date': datetime.strptime(date, '%Y-%m-%d').date(), 'token_assigned': last_appointment_token + 1}, partial=True)
            
            if serializer.is_valid():
                serializer.save()
            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return response.Response('Failed to change appointment status for the patient', status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response('Successfully changed appointment status for the patient.', status=status.HTTP_200_OK)


class GetPreviousAppointments(views.APIView):
    '''
        On a successful post request, returns the previous appointments for a patient
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        patient_id = request.data['id']
        patient = PatientUser.objects.get(id=patient_id)

        appointments = Appointment.objects.filter(patient=patient)
        resp = []

        for appointment in appointments:
            resp.append({'appointment_id': appointment.id, 'doctor_name': f'{appointment.doctor.user.first_name} {appointment.doctor.user.last_name}', 'doctor_id': appointment.doctor.id, 'appointment_date': appointment.date})

        return response.Response(resp, status=status.HTTP_202_ACCEPTED)
    


class GetUnpaidAppointments(views.APIView):
    '''
        On a successful post request, returns unpaid appointments for a doctor
    '''
    authentication_classes = (authentication.CustomFrontDeskAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def getTotalCost(self, prescription):
        total_cost = 0

        # Doctor Cost
        doctor_cost = prescription.appointment.doctor.consultation_fee
        total_cost += doctor_cost

        # Lab Tests costs
        lab_tests_cost = sum(
            lab_test.lab_test.test_cost for lab_test in prescription.lab_tests.all() if lab_test.status != 'Prescribed'
        )
        total_cost += lab_tests_cost

        # Medicines Cost
        medicines_cost = prescription.medicines_cost
        total_cost += medicines_cost

        return {
            'doctor_cost': doctor_cost,
            'lab_tests_cost': lab_tests_cost,
            'medicines_cost': medicines_cost,
            'total_cost': total_cost
        }

    def post(self, request):
        try:
            doctor = DoctorUser.objects.get(id=request.data['doctor_id'])
        except ObjectDoesNotExist:
            return response.Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        prescriptions = Prescription.objects.filter(appointment__doctor=doctor, paid=False)

        resp = [
            {
                'id': prescription.id,
                'patient_name': f'{prescription.appointment.patient.first_name} {prescription.appointment.patient.last_name}',
                'age': prescription.appointment.patient.age,
                'gender': prescription.appointment.patient.gender,
                'cost': self.getTotalCost(prescription)
            }
            for prescription in prescriptions
        ]

        return response.Response(resp, status=status.HTTP_200_OK)