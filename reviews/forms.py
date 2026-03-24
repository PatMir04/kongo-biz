from django import forms
from .models import Review, ReviewFlag, BusinessFlag


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Partagez votre experience...'
            }),
        }
        labels = {
            'rating': 'Note',
            'comment': 'Commentaire',
        }


class ReviewFlagForm(forms.ModelForm):
    class Meta:
        model = ReviewFlag
        fields = ('reason', 'description')
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Decrivez le probleme...'
            }),
        }
        labels = {
            'reason': 'Raison du signalement',
            'description': 'Details',
        }


class BusinessFlagForm(forms.ModelForm):
    class Meta:
        model = BusinessFlag
        fields = ('reason', 'description')
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Decrivez le probleme...'
            }),
        }
        labels = {
            'reason': 'Raison du signalement',
            'description': 'Details',
        }
