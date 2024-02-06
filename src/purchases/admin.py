from django.contrib import admin

# Register your models here.
from .models import Purchase, ChatLog

admin.site.register(Purchase)
admin.site.register(ChatLog)