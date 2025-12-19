from django import forms
from .models import Commande


class CommandeForm(forms.ModelForm):
    """
    ModelForm for creating and editing Commande instances.
    """
    class Meta:
        model = Commande
        fields = "__all__"
        widgets = {
            'Description_cmd': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez une description pour votre commande'
            }),
            'Date_cmd': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'Produit_cmd': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'Description_cmd': 'Description de la commande',
            'Date_cmd': 'Date de la commande',
            'Produit_cmd': 'Produit commandé',
        }
