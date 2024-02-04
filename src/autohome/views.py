from django.shortcuts import render, redirect
from queries import fetch_data, extract_text_from_url_pdf

from products.forms import VehicleForm

def home_view(request):
    context = {}
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        data = fetch_data(obj.vin)
        url = f"https://cdn.dealereprocess.org/cdn/servicemanuals/{data['make']}/{data['year']}-{data['model']}.pdf"
        extract_text_from_url_pdf(url, data['vehicle_handle'], obj)
        request.session['vehicle_id'] = obj.vin
        request.session['vehicle_name'] = data['vehicle_model']
        return redirect('/products/', data)
    context['form'] = form
    return render(request, "home.html", context)