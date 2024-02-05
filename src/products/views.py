from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import ProductForm, VehicleUpdateForm
from .models import Product, Vehicle

def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('/products/create/')
        form.add_error("You must be logged in to create products")
    context['form'] = form
    return render(request, 'products/create.html', context)

def product_list_view(request):
    object_list = Product.objects.exclude(pk=3)
    vin = request.session.get('vehicle_id')
    vehicle_name = request.session.get('vehicle_name')
    context = {
        "object_list": object_list,
        "vin": vin,
        "vehicle_name": vehicle_name
    }
    return render(request, "products/list.html", context)

def product_detail_view(request, handle=None):
    vin = request.session.get('vehicle_id')
    obj = get_object_or_404(Product, handle=handle)
    vehicle = get_object_or_404(Vehicle, handle=vin)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = request.user.purchase_set.all().filter(product=obj, completed=True).exists()
    context = {
        "object": obj,
        "vin": vin
        }
    if not is_owner:
        form = VehicleUpdateForm(request.POST or None, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.product = obj
            vehicle.save()
            return redirect('/products/checkout/')
        context['form'] = form
    return render(request, 'products/detail.html', context)

def checkout(request):
    context = {}
    return render(request, 'products/checkout.html', context)