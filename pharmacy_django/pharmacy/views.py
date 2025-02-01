from rest_framework import views, response, status, permissions, exceptions
from administrator.serializers import UserSerializer
from administrator import authentication

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


class GetCompletedPatients(views.APIView):
    '''
        In a get request, returns all the patients for whom medicines are to be given
    '''

    def get(self, request):
        pass

class Logout(views.APIView):
    '''
        Logout view can only be accessed by authenticated users
    '''
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        
        return response.Response("Successfully logged out user.")