from rest_framework import serializers, exceptions
from .models import Ingredients, Categories, SideEffects, Allergens, Medicines, MedicineStock, LabTests, UnlistedMedicine, UnlistedLabTest

class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Ingredients
        fields = '__all__'
        
    def create(self, validated_data):
        
        object = Ingredients.objects.create(**validated_data)
        
        return object
    

class CategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Categories
        fields = '__all__'
        
    def create(self, validated_data):
        
        object = Categories.objects.create(**validated_data)

        return object
    
    
class SideEffectsSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = SideEffects
        fields = '__all__'
        
    def create(self, validated_data):
        
        object = SideEffects.objects.create(**validated_data)
        
        return object
    

class AllergensSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Allergens
        fields = '__all__'
        
    def create(self, validated_data):
        
        object = Allergens.objects.create(**validated_data)
        return object
    

class MedicinesSerializer(serializers.ModelSerializer):
    
    # Check how ingredients are saved when multiple ingredients are saved and also how many=True works
    ingredients = IngredientsSerializer(many=True, required = False)
    allergens = AllergensSerializer(many=True, required = False)
    sideEffects = SideEffectsSerializer(many=True, required = False)
    categories = CategoriesSerializer(many=True, required = False)
    
    class Meta:
        
        model = Medicines
        fields = '__all__'
        
    def create(self, validated_data):
        
        ingredients_data = validated_data.pop('ingredients', None)
        categories_data = validated_data.pop('categories', None)
        sideEffects_data = validated_data.pop('sideEffects', None)
        allergens_data = validated_data.pop('allergens', None)

        # Validation for required many-to-many fields
        if not categories_data or not sideEffects_data or not allergens_data:
            raise serializers.ValidationError("All required fields are not provided.")

        # Create the medicine instance
        medicine = Medicines.objects.create(**validated_data)

        # Handle many-to-many relationships
        if ingredients_data:
            ingredients = [Ingredients.objects.get_or_create(**ingredient_data)[0] for ingredient_data in ingredients_data]
            medicine.ingredients.set(ingredients)  # Use `.set()` for many-to-many field assignment

        if categories_data:
            categories = [Categories.objects.get_or_create(**category_data)[0] for category_data in categories_data]
            medicine.categories.set(categories)

        if sideEffects_data:
            side_effects = [SideEffects.objects.get_or_create(**sideEffect_data)[0] for sideEffect_data in sideEffects_data]
            medicine.side_effects.set(side_effects)

        if allergens_data:
            allergens = [Allergens.objects.get_or_create(**allergy_data)[0] for allergy_data in allergens_data]
            medicine.allergens.set(allergens)

        return medicine
    

class MedicineStockSerializer(serializers.ModelSerializer):
    medicine = MedicinesSerializer(many=False, required=True)

    class Meta:
        model = MedicineStock
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested medicine data
        medicine_data = validated_data.pop('medicine')
        
        # Extract and handle many-to-many fields from medicine data
        ingredients_data = medicine_data.pop('ingredients', [])
        categories_data = medicine_data.pop('categories', [])
        sideEffects_data = medicine_data.pop('sideEffects', [])
        allergens_data = medicine_data.pop('allergens', [])
        
        # Create the Medicine instance
        medicine = Medicines.objects.create(**medicine_data)

        if ingredients_data:
            ingredients = [Ingredients.objects.get_or_create(**ingredient_data)[0] for ingredient_data in ingredients_data]
            medicine.ingredients.set(ingredients)

        if categories_data:
            categories = [Categories.objects.get_or_create(**category_data)[0] for category_data in categories_data]
            medicine.categories.set(categories)

        if sideEffects_data:
            side_effects = [SideEffects.objects.get_or_create(**sideEffect_data)[0] for sideEffect_data in sideEffects_data]
            medicine.side_effects.set(side_effects)

        if allergens_data:
            allergens = [Allergens.objects.get_or_create(**allergy_data)[0] for allergy_data in allergens_data]
            medicine.allergens.set(allergens)

        # Add the Medicine instance to validated_data and create the MedicineStock object
        validated_data['medicine'] = medicine

        try:
            medicine_stock = MedicineStock.objects.create(**validated_data)
            return medicine_stock
        except Exception as e:
            medicine.delete()  # Cleanup created Medicine object on failure
            raise serializers.ValidationError('Failed to create medicine stock object.')


class LabTestsSerializer(serializers.ModelSerializer):

    class Meta:

        model = LabTests
        fields = '__all__'


class UnlistedMedicinesSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnlistedMedicine
        fields = '__all__'
    

class UnlistedLabTestsSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnlistedLabTest
        fields = '__all__'