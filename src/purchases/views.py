from django.shortcuts import render
from django.conf import settings

base = settings.PROTECTED_MEDIA_ROOT

# Create your views here.
from products.models import Vehicle
from queries import create_embeddings

def chat_view(request):
    vehicle = Vehicle.objects.filter(handle='JF2SKASC2KH496845').first()

    create_embeddings(f'{base}/manuals/2019subaruforester.txt', '2019subaruforester', vehicle)


    return render(request, 'purchases/chat.html')