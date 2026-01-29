from django import forms
from .models import Animal, MedicalVisit, MedicalDocument


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'imie',
            'gatunek',
            'rasa',
            'wiek',
            'data_oszacowania_wieku',
            'data_przyjecia',
            'stan_zdrowia',
            'kondycja_ciala',
            'opis_charakteru',
            'status',
            'zdjecie',
        ]
        widgets = {
            # HTML5 datepicker
            'data_oszacowania_wieku': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'data_przyjecia': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class MedicalVisitForm(forms.ModelForm):
    class Meta:
        model = MedicalVisit
        fields = [
            'visit_date',
            'vet_name',
            'reason',
            'diagnosis',
            'treatment',
            'notes',
            'cost',
            'next_visit_date',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'next_visit_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ['title', 'document_date', 'file', 'notes']
        widgets = {
            'document_date': forms.DateInput(attrs={'type': 'date'}),
        }


