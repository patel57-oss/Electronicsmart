from django import forms
from .models import Product, Feedback, ContactFeedback


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'name',
            'price',
            'brand',
            'description',
            'image',
            'stock',
            'slug',
            'category',
            'subcategory']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your feedback...'}),
        }


class ContactFeedbackForm(forms.ModelForm):
    class Meta:
        model = ContactFeedback
        fields = ['name', 'email', 'mobile', 'review']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your mobile number',
                'required': True
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your feedback, suggestions, or reviews...',
                'required': True
            }),
        }
