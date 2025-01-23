from django.shortcuts import render
from rest_framework import views, response, status, permissions, exceptions

from administrator.models import User
from doctor.models import SpecializationAvailable

from administrator.serializers import UserSerializer
from doctor.serializers import SpecializationSerializer

from administrator import authentication
from pharmacy.models import Medicines, Allergens, SideEffects, Ingredients, Categories, MedicineStock, LabTests
from pharmacy.serializers import MedicinesSerializer, AllergensSerializer, CategoriesSerializer, IngredientsSerializer, SideEffectsSerializer, MedicineStockSerializer, LabTestsSerializer

class SignIn(views.APIView):
    '''
        API view for administrator signin
    '''
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        '''
            Only post methods are allowed for this endpoint.
            The data posted is stored in User model.
        '''
        
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            if user.is_verified == False or user.is_superuser == False:
                return exceptions.AuthenticationFailed("Sign In user details must be of a admin.")
            
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class EditProfile(views.APIView):
    '''
        API View for editing profile details for administrator
    '''
    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        user = request.user

        serializer = UserSerializer(user, data=request.data)

        return response.Response("Successfully edited user profile.")


class VerifyEmployees(views.APIView):
    
    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        unverifiedEmployees = User.objects.filter(is_verified=False)
        
        resp = []
            
        for user in unverifiedEmployees:
            user_serializer = UserSerializer(user)
            resp.append(user_serializer.data)
            
        return response.Response(resp)
    
    def post(self, request):
        
        # Credentials of the user to be set to verified
        ids = request.data['ids']
        code = request.data['code']
        
        try:
            for id in ids:
                user = User.objects.get(id=id)
                if code == 0:
                    user.is_verified = True
                    user.save()
                elif code == 1:
                    user.delete()
        except:
            return exceptions.NotAcceptable('Failed to delete users.')
        
        if code == 0:
            return response.Response('Users successfully verified.')
        elif code == 1:
            return response.Response('Users succesfully deleted.')
        else:
            return exceptions.NotAcceptable('The code provided is not a valid code.')
        

class ViewEmployees(views.APIView):
    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        users = User.objects.exclude(is_superuser=True)
        
        resp = []
        
        for user in users:
            user_serializer = UserSerializer(user)
            resp.append(user_serializer.data)
            
        return response.Response(resp)
    
    def post(self, request):
        
        ids = request.data['ids']
        
        try:
            for id in ids:
                user = User.objects.get(id=id)
                user.delete()
        except:
            return exceptions.NotAcceptable('Failed to delete users.')
            
        return response.Response('Users successfully deleted from system.')


class ViewMedicines(views.APIView):
    '''
        When it's a get request, this API returns all the medicines available
        When it's a post request, this API allows to delete the medicine
    '''
    
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        medicines = Medicines.objects.all()
        
        resp = []
        
        for medicine in medicines:
            medicine_serialized = MedicinesSerializer(medicine)
            resp.append(medicine_serialized.data)
        
        return response.Response(resp)
    
    def post(self, request):
        
        try:

            for id in request.data['ids']:
            
                medicine = Medicines.objects.get(id=id)
                medicineStocks = MedicineStock.objects.filter(medicine=medicine)
                
                medicineStocks.delete()
                medicine.delete()
            
            return response.Response({"message": "Medicine updated successfully."}, status=status.HTTP_200_OK)
            
        except Medicines.DoesNotExist:
            return response.Response({"error": "Medicine not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    

class AddMedicines(views.APIView):
    '''
        Add Medicines endpoint
        When it's a get request, it returns the medicines, ingredients, and alleriges available in the database already
        When it's a post request, it makes the necessary entries into the inter-dependent tables (like ingredients) and then makes the entry into the Medicines table.
    '''
    
    authentication_classes = (authentication.CustomAdminAuthentication, authentication.CustomPharmacyAuthentication)
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        allergens = Allergens.objects.all()
        ingredients = Ingredients.objects.all()
        sideEffects = SideEffects.objects.all()
        categories = Categories.objects.all()
        
        resp = {
            'allergens': [],
            'ingredients': [],
            'sideEffects': [],
            'categories': []
        }
        
        for allergy in allergens:
            serialized = AllergensSerializer(allergy)
            resp['allergens'].append(serialized.data)
            
        for ingredient in ingredients:
            serialized = IngredientsSerializer(ingredient)
            resp['ingredients'].append(serialized.data)
            
        for sideEffect in sideEffects:
            serialized = SideEffectsSerializer(sideEffect)
            resp['sideEffects'].append(serialized.data)
            
        for category in categories:
            serialized = CategoriesSerializer(category)
            resp['categories'].append(serialized.data)
            
        return response.Response(resp)


    def post(self, request):
        
        serializer = MedicineStockSerializer(data=request.data)

        if serializer.is_valid():
            medicineStock = serializer.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class SpecializationAvailableView(views.APIView):
    '''
        In a get request, returns all specializations available
        In a post request, can make new entires into the SpecializationAvailable model
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):

        objects = SpecializationAvailable.objects.all()

        resp = []

        for object in objects:
            object_serializer = SpecializationSerializer(object)
            resp.append(object_serializer.data)

        return response.Response(resp)
    
    def post(self, request):
        
        serializer = SpecializationSerializer(data=request.data)

        if serializer.is_valid():
            specialization = serializer.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddLabTest(views.APIView):
    '''
        In a successful post request, an object of LabTest is made
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        serializer = LabTestsSerializer(data=request.data)

        if serializer.is_valid():
            labTest = serializer.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ViewLabTests(views.APIView):
    '''
        In a get request, all the labtests available are  
    '''
    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):

        labTests = LabTests.objects.all()

        resp = []

        for labTest in labTests:
            serializer = LabTestsSerializer(labTest)

            resp.append(serializer.data)

        return response.Response(resp)


class Logout(views.APIView):
    '''
        Logout view can only be accessed by authenticated users
    '''
    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        resp = response.Response()
        # resp.delete_cookie("jwt")
        
        resp.data = {"message": "Successfully logged out user."}
        
        return resp