from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone

PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    # stripe_product_id =
    name = models.CharField(max_length=120)
    handle = models.SlugField(unique=True) # slug
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.95)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.95)
    # stripe_price_id =
    stripe_price = models.IntegerField(default=995) # 100 * price
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price != self.og_price:
            # price changed
            self.og_price = self.price
            # trigger an API request for the price
            self.stripe_price = int(self.price * 100)
            self.price_changed_timestamp = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/products/{self.handle}/"

class Vehicle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    vin = models.CharField(max_length=17)
    handle = models.SlugField(unique=True) # slug
    product = models.ForeignKey(Product, default=3, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.handle = self.vin
        super().save(*args, **kwargs)

def handle_vehicle_attachment_upload(instance, filename):
    return f"products/{instance.vehicle.handle}/attachments/{filename}"

class VehicleAttachment(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments/", blank=True, null=True)
    storage = protected_storage
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)