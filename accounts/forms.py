from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresse email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prenom'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom de famille'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cette adresse email est deja utilisee.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'city', 'phone', 'is_business_owner')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Parlez-nous de vous...'
            }),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+243 ...'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'is_business_owner': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
