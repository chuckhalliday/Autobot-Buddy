from django.db import models
from django.conf import settings
from django.utils import timezone

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
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    product = models.ForeignKey(Product, default=3, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.handle = self.vin
        super().save(*args, **kwargs)