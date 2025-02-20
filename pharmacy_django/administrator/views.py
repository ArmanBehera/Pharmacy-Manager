from django.db.models import Count
from rest_framework import views, response, status, permissions, exceptions

from .models import User
from . import authentication

from doctor.models import SpecializationAvailable, DoctorUser
from pharmacy.models import Medicines, Allergens, SideEffects, Ingredients, Categories, MedicineStock, LabTests

from pharmacy.serializers import MedicinesSerializer, AllergensSerializer, CategoriesSerializer, IngredientsSerializer, SideEffectsSerializer, MedicineStockSerializer, LabTestsSerializer
from administrator.serializers import UserSerializer
from doctor.serializers import SpecializationSerializer

from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

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

        if serializer.is_valid():
            serializer.save()

        return response.Response("Successfully edited user profile.")


class VerifyEmployees(views.APIView):
    
    '''
        In a get request, returns all the unverified employees
        In a post requets, tries to verify the user whose ids are submitted
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        unverified_employees = User.objects.filter(is_verified=False)

        return response.Response(UserSerializer(unverified_employees, many=True).data)
    
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


class EditEmployees(views.APIView):
    '''
        In a post request, deletes or unverifies the employees whose ids are submitted
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        ids = request.data['ids']
        code = request.data['code']

        # Deleting user
        if code == 0:
            try:
                for id in ids:
                    user = User.objects.get(id=id)
                    user.delete()
            except Exception as e:
                return response.Response(e, status=status.HTTP_400_BAD_REQUEST)
                
            return response.Response('Users successfully deleted from system.')
        
        # Unverifying user
        elif code == 1:
            try:
                for id in ids:
                    user = User.objects.get(id=id)
                    user.is_verified = False
                    user.save()
            except Exception as e:
                return response.Response(e, status=status.HTTP_400_BAD_REQUEST)
            
            return response.Response('Users successfully unverified.')

class GetMedicines(views.APIView):
    '''
        When it's a get request, this API returns all the medicines available
    '''
    
    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        
        medicine_stocks = MedicineStock.objects.all().order_by('medicine__name')

        return response.Response(MedicineStockSerializer(medicine_stocks, many=True).data)
    
    def post(self, request):

        medicine_stocks = MedicineStock.objects.filter(medicine__name__icontains=request.data['name']).order_by('medicine__name')

        return response.Response(MedicineStockSerializer(medicine_stocks, many=True).data)


class GetUniqueMedicines(views.APIView):
    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        
        medicine_stocks = MedicineStock.objects.all()  # Fetch all medicine stocks

        unique_medicines = []
        seen_medicine_names = set()

        for stock in medicine_stocks:
            if stock.medicine.name not in seen_medicine_names:
                unique_medicines.append(MedicineStockSerializer(stock).data)
                seen_medicine_names.add(stock.medicine.name)  # Track seen names

        return response.Response(unique_medicines, status=status.HTTP_202_ACCEPTED)
    
    def post(self, request):

        medicine_stocks = MedicineStock.objects.filter(medicine__name__icontains=request.data['name'])

        unique_medicines = []
        seen_medicine_names = set()

        for stock in medicine_stocks:
            if stock.medicine.name not in seen_medicine_names:
                unique_medicines.append(MedicineStockSerializer(stock).data)
                seen_medicine_names.add(stock.medicine.name)  # Track seen names

        return response.Response(unique_medicines, status=status.HTTP_202_ACCEPTED)


class AddMedicines(views.APIView):
    '''
        Add Medicines endpoint
        When it's a get request, it returns the medicines, ingredients, and alleriges available in the database already
        When it's a post request, it makes the necessary entries into the inter-dependent tables (like ingredients) and then makes the entry into the Medicines table.
    '''
    
    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        allergens = Allergens.objects.all()
        ingredients = Ingredients.objects.all()
        side_effects = SideEffects.objects.all()
        categories = Categories.objects.all()
        
        resp = {
            'allergens': [],
            'ingredients': [],
            'side_effects': [],
            'categories': []
        }
        
        for allergy in allergens:
            serialized = AllergensSerializer(allergy)
            resp['allergens'].append(serialized.data)
            
        for ingredient in ingredients:
            serialized = IngredientsSerializer(ingredient)
            resp['ingredients'].append(serialized.data)
            
        for side_effect in side_effects:
            serialized = SideEffectsSerializer(side_effect)
            resp['side_effects'].append(serialized.data)
            
        for category in categories:
            serialized = CategoriesSerializer(category)
            resp['categories'].append(serialized.data)
            
        return response.Response(resp)


    def post(self, request):
        
        serializer = MedicineStockSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddMedicineStock(views.APIView):

    '''
        In a successful post request, a new Medicine Stock objet is created
    '''

    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
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

    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        try:
            for id in request.data['ids']:
            
                medicine_stocks = MedicineStock.objects.filter(id=id)
                
                for medicine_stock in medicine_stocks:

                    medicine = medicine_stock.medicine
                
                    medicine_stock.delete()
                    medicine.delete()
            
            return response.Response({"message": "Medicine deleted successfully."}, status=status.HTTP_200_OK)
            
        except Medicines.DoesNotExist:
            return response.Response({"error": "Medicine not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GetSpecializationAvailable(views.APIView):
    '''
        In a get request, returns all specializations available
        In a post request, filters the specializations returned according to the name given
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):

        specializations = SpecializationAvailable.objects.all()

        resp = []

        for specialization in specializations:
            number = DoctorUser.objects.filter(specialization=specialization).count()
            resp.append({'id': specialization.id, 'specialization': specialization.specialization, 'number': number})

        return response.Response(resp)

    def post(self, request):

        specializations = SpecializationAvailable.objects.filter(specialization__icontains=request.data['name'])

        resp = []

        for specialization in specializations:
            number = DoctorUser.objects.filter(specialization=specialization).count()
            resp.append({'id': specialization.id, 'specialization': specialization.specialization, 'number': number})

        return response.Response(resp)


class AddSpecializationAvailable(views.APIView):
    '''
        In a post request, can make new entires into the SpecializationAvailable model
    '''

    authentication_classes = (authentication.CustomAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def post(self, request):
        
        serializer = SpecializationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

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
            
                specialization_available = SpecializationAvailable.objects.get(id=id)
                specialization_available.delete()
            
            return response.Response({"message": "Specialization deleted successfully."}, status=status.HTTP_200_OK)
            
        except SpecializationAvailable.DoesNotExist:
            return response.Response({"error": "SpecializationAvailable object not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GetLabTests(views.APIView):
    '''
        In a get request, all the labtests object available are returned
    '''
    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):

        lab_tests = LabTests.objects.all()

        return response.Response(LabTestsSerializer(lab_tests, many=True).data)
    
    def post(self, request):

        lab_tests = LabTests.objects.filter(name__icontains=request.data['name'])

        return response.Response(LabTestsSerializer(lab_tests, many=True).data)


class AddLabTests(views.APIView):
    '''
        In a successful post request, an object of LabTest is made
    '''

    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        serializer = LabTestsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditLabTests(views.APIView):
    '''
        In a successful post request, an already existing object of LabTest is update.
    '''

    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        lab_test = LabTests.objects.get(id=request.data['id'])
        serializer = LabTestsSerializer(lab_test, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else: 
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class DeleteLabTests(views.APIView):

    '''
        In a post request, delete the labtests whose indexes are submitted in the authentication classes. 
    '''

    authentication_classes = (authentication.CombinedPharmacyAndAdminAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        
        try:
            for id in request.data['ids']:
            
                lab_test = LabTests.objects.get(id=id)
                lab_test.delete()
            
            return response.Response({"message": "LabTest deleted successfully."}, status=status.HTTP_200_OK)
            
        except LabTests.DoesNotExist:
            return response.Response({"error": "LabTest object not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
