from django import forms
from .models import Business


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'name', 'category', 'description', 'address', 'city',
            'commune', 'phone', 'whatsapp', 'email', 'website',
            'image', 'opening_hours', 'latitude', 'longitude',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'opening_hours': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Lun-Ven: 8h-18h\nSam: 9h-14h'}),
            'name': forms.TextInput(attrs={'placeholder': 'Nom de votre entreprise'}),
            'address': forms.TextInput(attrs={'placeholder': 'Adresse complete'}),
            'phone': forms.TextInput(attrs={'placeholder': '+243 XXX XXX XXX'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+243 XXX XXX XXX'}),
        }


class BusinessSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'restaurants, pharmacies, hotels...',
            'class': 'form-control form-control-lg',
        })
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Kinshasa, Lubumbashi...',
            'class': 'form-control form-control-lg',
        })
    )
