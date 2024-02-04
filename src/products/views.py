from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import ProductForm, ProductUpdateForm
from .models import Product

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
    obj = get_object_or_404(Product, handle=handle)
    vin = request.session.get('vehicle_id')
    is_owner = False
    if request.user.is_authenticated:
        is_owner = obj.user == request.user
    context = {
        "object": obj,
        "vin": vin
        }
    if is_owner:
        form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            # return redirect('/products/create/')
        context['form'] = form
    return render(request, 'products/detail.html', context)