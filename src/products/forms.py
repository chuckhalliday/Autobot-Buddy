from django import forms
from .models import Product, Vehicle, VehicleAttachment

input_css_class = "form-control"

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vin'].widget.attrs.update({'class': input_css_class})
        self.fields['vin'].label = 'VIN'

    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        if len(vin) != 17:
            raise forms.ValidationError("VIN must be exactly 17 characters long.")
        return vin
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class