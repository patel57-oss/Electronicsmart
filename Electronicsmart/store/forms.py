from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'price', 'stock', 'description', 'image', 'category', 'slug']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
