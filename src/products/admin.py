from django.contrib import admin

# Register your models here.
from .models import Product, Vehicle, VehicleAttachment, File

admin.site.register(File)
admin.site.register(Product)
admin.site.register(Vehicle)
admin.site.register(VehicleAttachment)