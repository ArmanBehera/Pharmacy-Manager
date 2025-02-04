from django.contrib import admin
from .models import Ingredients, Categories, SideEffects, Allergens, Medicines, MedicineStock, LabTests

# Register your models here.
admin.site.register(Ingredients)
admin.site.register(Categories)
admin.site.register(SideEffects)
admin.site.register(Allergens)
admin.site.register(Medicines)
admin.site.register(MedicineStock)
admin.site.register(LabTests)