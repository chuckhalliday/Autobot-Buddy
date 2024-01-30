from django.shortcuts import render, redirect

from products.forms import VehicleForm

def home_view(request):
    context = {}
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        request.session['vehicle_id'] = obj.vin
        return redirect('/products/')
    context['form'] = form
    return render(request, "home.html", context)