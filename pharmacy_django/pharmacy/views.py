from rest_framework import views, response, status, permissions, exceptions


from administrator.serializers import UserSerializer
from administrator import authentication

from doctor.models import DoctorUser, Prescription, PrescribedLabTest, Appointment
from doctor.serializers import PrescriptionSerializer, AppointmentSerializer

from .models import LabTests
from .serializers import LabTestsSerializer

from django.utils import timezone

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
        
        if request.data['role'] != 'Pharmacy':
            return response.Response('Failed to create pharmacy user. Role should be assigned pharmacy.')

        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDoctors(views.APIView):
    '''
        Get view is used to retun all the doctors
    '''
    authentication_classes = (authentication.CustomPharmacyAuthentication, )
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


class Logout(views.APIView):
    '''
        Logout view can only be accessed by authenticated users
    '''
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        
        return response.Response("Successfully logged out user.")