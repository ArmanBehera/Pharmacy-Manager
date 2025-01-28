from django.shortcuts import render
from rest_framework import views, response, status, permissions, exceptions

from administrator.models import User
from doctor.models import SpecializationAvailable, DoctorUser
from pharmacy.models import Medicines, Allergens, SideEffects, Ingredients, Categories, MedicineStock, LabTests

from pharmacy.serializers import MedicinesSerializer, AllergensSerializer, CategoriesSerializer, IngredientsSerializer, SideEffectsSerializer, MedicineStockSerializer, LabTestsSerializer
from administrator.serializers import UserSerializer
from doctor.serializers import SpecializationSerializer

from administrator import authentication

from datetime import datetime

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
    
    '''
        In a get request, returns all the unverified employees
        In a post requets, tries to verify the user whose ids are submitted
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        unverifiedEmployees = User.objects.filter(is_verified=False)

        return response.Response(UserSerializer(unverifiedEmployees, many=True).data)
    
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
            return exceptions.NotAcceptable('Failed to verify users.')
        
        if code == 0:
            return response.Response('Users successfully verified.')
        elif code == 1:
            return response.Response('Users succesfully deleted.')
        else:
            return exceptions.NotAcceptable('The code provided is not a valid code.')
        

class GetEmployees(views.APIView):
    '''
        In a get request, returns all the employees in the system
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        users = User.objects.exclude(is_superuser=True)
            
        return response.Response(UserSerializer(users, many=True).data)


class DeleteEmployees(views.APIView):
    '''
        In a post request, deletes the employees whose ids are submitted
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        ids = request.data['ids']
        
        try:
            for id in ids:
                user = User.objects.get(id=id)
                user.delete()
        except:
            return exceptions.NotAcceptable('Failed to delete users.')
            
        return response.Response('Users successfully deleted from system.')

class GetMedicines(views.APIView):
    '''
        When it's a get request, this API returns all the medicines available
    '''
    
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        medicines = MedicineStock.objects.all()

        return response.Response(MedicineStockSerializer(medicines, many=True).data)

    def post(self, request):

        medicineStocks = MedicineStock.objects.filter(medicine__name__icontains=request.data['name'])

        return response.Response(MedicineStockSerializer(medicineStocks, many=True).data)


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


class AddMedicineStock(views.APIView):

    '''
        In a successful post request, a new Medicine Stock objet is created
    '''

    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        medicine = Medicines.objects.get(id=request.data['id'])

        try: 
            MedicineStock.objects.create(medicine=medicine, stock=request.data['stock'], expiration_date=datetime.strptime(request.data['expiration_date'], "%Y-%m-%d").date())
        except:
            return response.Response('Unable to add stock.', status=status.HTTP_400_BAD_REQUEST)

        return response.Response('Added stock for medicine.', status=status.HTTP_201_CREATED)


# Faulty. Need to debug this.
class DeleteMedicines(views.APIView):
    '''
        When it's a post request, deletes the medicines whose ids are submitted
    '''

    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

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


class GetSpecializationAvailable(views.APIView):
    '''
        In a get request, returns all specializations available
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):

        objects = SpecializationAvailable.objects.all()

        return response.Response(SpecializationSerializer(objects,  many=True).data)


class AddSpecializationAvailable(views.APIView):

    '''
        In a post request, can make new entires into the SpecializationAvailable model
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def post(self, request):
        
        serializer = SpecializationSerializer(data=request.data)

        if serializer.is_valid():
            specialization = serializer.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EditSpecializationAvailable(views.APIView):
    '''
        In a successful post request, an already existing object of LabTest is update.
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        specializationAvailable = SpecializationAvailable.objects.get(id=request.data['id'])
        serializer = SpecializationSerializer(specializationAvailable, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else: 
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)



class DeleteSpecializationAvailable(views.APIView):

    '''
        In a post request, delete the labtests whose indexes are submitted in the authentication classes. 
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        try:
            for id in request.data['ids']:
            
                specializationAvailable = SpecializationAvailable.objects.get(id=id)
                specializationAvailable.delete()
            
            return response.Response({"message": "Specialization deleted successfully."}, status=status.HTTP_200_OK)
            
        except LabTests.DoesNotExist:
            return response.Response({"error": "SpecializationAvailable object not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GetLabTests(views.APIView):
    '''
        In a get request, all the labtests object available are returned
    '''
    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):

        labTests = LabTests.objects.all()

        return response.Response(LabTestsSerializer(labTests, many=True).data)


class AddLabTests(views.APIView):
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


class EditLabTests(views.APIView):
    '''
        In a successful post request, an already existing object of LabTest is update.
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        labtest = LabTests.objects.get(id=request.data['id'])
        serializer = LabTestsSerializer(labtest, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else: 
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class DeleteLabTests(views.APIView):

    '''
        In a post request, delete the labtests whose indexes are submitted in the authentication classes. 
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        try:
            for id in request.data['ids']:
            
                labTest = LabTests.objects.get(id=id)
                labTest.delete()
            
            return response.Response({"message": "LabTest deleted successfully."}, status=status.HTTP_200_OK)
            
        except LabTests.DoesNotExist:
            return response.Response({"error": "LabTest object not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class Logout(views.APIView):
    '''
        Logout view can only be accessed by authenticated users
    '''
    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request):
        
        return response.Response("Successfully logged out user.")