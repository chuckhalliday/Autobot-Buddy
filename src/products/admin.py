from django.contrib import admin

# Register your models here.
from .models import Product, Vehicle, VehicleAttachment

admin.site.register(Product)
admin.site.register(Vehicle)
admin.site.register(VehicleAttachment)