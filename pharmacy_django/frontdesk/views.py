from django.shortcuts import render
from rest_framework import views, response, status, permissions, exceptions
from administrator.serializers import UserSerializer
from administrator import authentication
from administrator.models import User
from doctor.models import DoctorUser, Appointment
from doctor.serializers import AppointmentSerializer

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


class AddPatient(views.APIView):
    '''
        View to add the preliminary details of the patient
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

    def post(self, request):
        # To add to the request: token_number: figure out the logic for that
        try:
            last_appointment_token = Appointment.objects.filter(doctor=request.data['doctor']).order_by('-token_assigned').first().token_assigned
        except Exception:
            last_appointment_token = 0

        serializer = AppointmentSerializer(data={**request.data, 'token_assigned': last_appointment_token + 1})

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
        