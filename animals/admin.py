from django.contrib import admin
from .models import Animal, MedicalVisit, MedicalDocument


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        'id_zwierzecia',   # klucz główny
        'imie',
        'gatunek',
        'status',
        'wiek',
    )
    search_fields = (
        'imie',
        'gatunek',
        'rasa',
    )
    list_filter = (
        'status',
        'gatunek',
    )

@admin.register(MedicalVisit)
class MedicalVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'visit_date', 'vet_name', 'cost')
    list_filter = ('visit_date',)
    search_fields = ('animal__imie', 'vet_name', 'reason', 'diagnosis')

@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'title', 'document_date', 'uploaded_at')
    list_filter = ('document_date', 'uploaded_at')
    search_fields = ('animal__imie', 'title', 'notes')

