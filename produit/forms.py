from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['Description_cmd', 'Date_cmd']
        widgets = {
            'Description_cmd': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez une description pour votre commande'
            }),
            'Date_cmd': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'Description_cmd': 'Description de la commande',
            'Date_cmd': 'Date de la commande',
        }

    def __init__(self, *args, **kwargs):
        super(CommandeForm, self).__init__(*args, **kwargs)
        # Remove the Produit_cmd field from the form since we're handling it manually
        if 'Produit_cmd' in self.fields:
            del self.fields['Produit_cmd']
