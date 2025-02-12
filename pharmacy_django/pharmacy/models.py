from django.db import models
from django.core.validators import MinValueValidator


class Ingredients(models.Model):
    '''
        Stores the ingredients information
    '''
    name = models.CharField(max_length=255, verbose_name="Ingredient Name", help_text="Name of the ingredient")

    def __str__(self):
        return self.name


class Categories(models.Model):
    '''
        Stores categories for medicines
    '''
    name = models.CharField(max_length=255, verbose_name="Category Name", help_text="Name of the category", blank=False)
    usage_priority = models.IntegerField(verbose_name="Usage Priority", help_text="Priority of this category for the medicine", blank=False)

    def __str__(self):
        return f"{self.name} (Priority: {self.usage_priority})"


class SideEffects(models.Model):
    '''
        Stores side effects of medicines
    '''
    name = models.CharField(max_length=255, verbose_name="Side Effect", help_text="Description of the side effect", blank=False)

    def __str__(self):
        return self.name


class Allergens(models.Model):
    '''
        Stores the Allergens of the medicine
    '''
    name = models.CharField(max_length=255, verbose_name="Allergens", help_text="Allergy for the medicines", blank=False)
    
    def __str__(self):
        return self.name


class Medicines(models.Model):
    '''
        Stores the medicines value
    '''

    TIMING_CHOICES = [
        ('Before Food', 'Before Food'),
        ('After Food', 'After Food'),
        ('Custom', 'Custom')
    ]
    
    name = models.CharField(max_length=255, verbose_name="Medicine Name", help_text="Name of the medicine", blank=False, unique=True)
    price = models.FloatField(validators=[MinValueValidator(0.0)], verbose_name="Price", help_text="Price of the medicine", blank=False)
    description = models.TextField(verbose_name="Description", blank=True, null=True, help_text="Description of the medicine")
    manufacturer = models.CharField(max_length=255, verbose_name="Manufacturer", help_text="Manufacturer of the medicine", blank=False)
    ingredients = models.ManyToManyField(Ingredients, verbose_name="Ingredients", help_text="Ingredients in the medicine", related_name="medicines", blank=True)
    categories = models.ManyToManyField(Categories, verbose_name="Categories", help_text="Categories of the medicine", related_name="medicines", blank=False)
    side_effects = models.ManyToManyField(SideEffects, verbose_name="Side Effects", help_text="Possible side effects of the medicine", related_name="medicines", blank=False)
    allergens = models.ManyToManyField(Allergens, verbose_name="Allergens", help_text="Patients with these allergies should avoid.", related_name="medicines", blank=False)
    timings = models.CharField(max_length=11, choices=TIMING_CHOICES, verbose_name="Timing", blank=False)
    custom_timing_description = models.TextField(blank=True, null=True, verbose_name="Description for Custom timing if selected")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Medicines"


class MedicineStock(models.Model):

    medicine = models.ForeignKey(Medicines, verbose_name="Medicine Details", on_delete=models.CASCADE, related_name="Medicine_Stock", blank=False, null=False)
    stock = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Stock", help_text="Stock quantity of the medicine", blank=False)
    expiration_date = models.DateField(verbose_name="Expiration Date", blank=False, help_text="Expiration date of the medicine")

    def __str__(self):
        return f"Medicine name: {self.medicine.name}. Expiration Date: {self.expiration_date}. Stock: {self.stock}"


class LabTests(models.Model):
    
    name = models.CharField(max_length=255, verbose_name="Test Name", blank=False)
    description = models.TextField(verbose_name="Test Description", blank=True, null=True)
    test_cost = models.FloatField(verbose_name="Test cost", blank=False)
    sample_required = models.CharField(max_length=100, verbose_name="Sample Required")
    pre_test_requirements = models.TextField(verbose_name="Pre-Test Requirements", blank=True, null=True)  
    provider = models.CharField(max_length=255, verbose_name="Provider for the lab test", blank=False)

    def __str__(self):
        return f"Test Name - {self.name}. Cost - {self.test_cost}"