# forms.py
from django import forms
from .models import Product
INPUT_CLASS = 'form-control'  # Replace 'form-control' with your actual CSS class

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'brand', 'price', 'description', 'image', 'stock']

from django import forms
from .models import Product

class EditproductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'description', 'price', 'image', 'stock')
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_sold': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
