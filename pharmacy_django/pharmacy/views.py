from rest_framework import views, response, status, permissions, exceptions


from administrator.serializers import UserSerializer
from administrator import authentication

from doctor.models import DoctorUser, Prescription, PrescribedLabTest, Appointment, PrescribedMedicine
from doctor.serializers import PrescriptionSerializer, AppointmentSerializer

from .models import LabTests, Medicines, MedicineStock
from .serializers import LabTestsSerializer, MedicinesSerializer

from django.utils import timezone

from datetime import date

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


class UpdateLabTests(views.APIView):
    '''
        Adds  details  for the prescribed lab tests, like test_date, status
    '''

    authentication_classes = (authentication.CustomPharmacyAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        today = date.today()
        data = request.data

        try:
            for i in range(len(data.get('id', []))):  # Ensure 'id' key exists
                prescribed_lab_test = PrescribedLabTest.objects.get(id=data['id'][i])

                # Update only if the keys exist and have valid indices
                prescribed_lab_test.test_date = today  # Always set test_date to today

                if 'sample_tracking_code' in data and i < len(data['sample_tracking_code']) and data['sample_tracking_code'][i]:
                    prescribed_lab_test.sample_tracking_code = data['sample_tracking_code'][i]

                if 'status' in data and i < len(data['status']) and data['status'][i]:
                    prescribed_lab_test.status = data['status'][i]

                if 'report_code' in data and i < len(data['report_code']) and data['report_code'][i]:
                    prescribed_lab_test.report_code = data['report_code'][i]

                prescribed_lab_test.save()

        except PrescribedLabTest.DoesNotExist:
            return response.Response({'error': 'Lab test not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except IndexError:
            return response.Response({'error': 'Mismatched list lengths in request data.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return response.Response({'message': 'Successfully edited lab test.'}, status=status.HTTP_202_ACCEPTED)


class UpdateStock(views.APIView):
    '''
        On a successful post request, updates the stock
    '''
    authentication_classes = (authentication.CustomPharmacyAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        try:
            prescription = Prescription.objects.get(id=request.data['prescription_id'])
            update_stock = request.data.get('update_stock', [])  # Extract update_stock list safely

            resp = []

            medicines_cost = prescription.medicines_cost

            for row in update_stock:
                try:
                    medicine = Medicines.objects.get(id=row['id'])
                    quantity = row['quantity']
                    medicine_stocks = MedicineStock.objects.filter(medicine=medicine).order_by('expiration_date')

                    while quantity > 0 and medicine_stocks.exists():
                        stock_entry = medicine_stocks.first()  # Get the earliest expiring stock
                        stock = stock_entry.stock

                        if stock <= quantity:
                            quantity -= stock
                            medicines_cost += medicine.price * stock
                            stock_entry.delete()  # Delete depleted stock
                        else:
                            stock_entry.stock -= quantity
                            medicines_cost += medicine.price * quantity
                            stock_entry.save()
                            quantity = 0  # Fully reduced, break loop
                    
                    prescribed_medicine = PrescribedMedicine.objects.filter(
                        prescription=prescription, 
                        medicine=medicine
                    ).first()

                    if prescribed_medicine:
                        if quantity == 0:
                            resp.append({"id": row['id'], "medicine_name": medicine.name, "status": "updated"})
                        else:
                            resp.append({"id": row['id'], "medicine_name": medicine.name, "status": "unavailable", "quantity": quantity})
                        
                        prescribed_medicine.save()

                except Medicines.DoesNotExist:
                    resp.append({"id": row['id'], "medicine_name": f"ID {row['id']}", "status": "Medicine Not Found."})

                except Exception as e:
                    resp.append({"id": row['id'], "medicine_name": f"ID {row['id']}", "status": f"Error: {str(e)}"})

            prescription.medicines_cost = medicines_cost
            prescription.save()

            return response.Response(resp, status=status.HTTP_200_OK)

        except Prescription.DoesNotExist:
            return response.Response({"error": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)