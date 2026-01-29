from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Animal(models.Model):
    id_zwierzecia = models.AutoField(primary_key=True, db_column='ID_zwierzecia')

    imie = models.CharField(max_length=50)
    gatunek = models.CharField(max_length=50)
    rasa = models.CharField(max_length=50)
    data_przyjecia = models.DateField()

    STATUS_CHOICES = [
        ('do_adopcji', 'Do adopcji'),
        ('w_trakcie', 'W trakcie adopcji'),
        ('adoptowany', 'Adoptowany'),
    ]

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='do_adopcji'
    )

    wiek = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(40)]
    )
    data_oszacowania_wieku = models.DateField(null=True, blank=True)
    stan_zdrowia = models.TextField(null=True, blank=True)
    kondycja_ciala = models.CharField(max_length=50, blank=True)
    opis_charakteru = models.CharField(max_length=50, blank=True)
    zdjecie = models.ImageField(upload_to='animals_photos/', blank=True, null=True)

    # <-- DODAJ / PRZENIEŚ TU
    opiekun = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='podopieczni'
    )

    class Meta:
        db_table = 'Zwierzeta'

    def __str__(self):
        return f"{self.imie} ({self.gatunek})"

    
class AnimalHistory(models.Model):
    """
    Pojedynczy wpis w historii zwierzaka (oś czasu).
    """
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='history'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)

    old_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    new_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.timestamp}: {self.action}"



class MedicalVisit(models.Model):
    """
    Wizyta medyczna zwierzęcia.
    """
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='medical_visits'
    )

    visit_date = models.DateField()
    vet_name = models.CharField(max_length=100, blank=True)
    reason = models.CharField(max_length=255, blank=True)        # powód wizyty
    diagnosis = models.TextField(blank=True)                     # rozpoznanie
    treatment = models.TextField(blank=True)                     # zalecenia / leczenie
    notes = models.TextField(blank=True)                         # dodatkowe notatki

    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    next_visit_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_date', '-created_at']

    def __str__(self):
        return f"Wizyta {self.animal.imie} ({self.visit_date})"

class MedicalDocument(models.Model):
    """
    Dokumentacja medyczna zwierzęcia (PDF/JPG/PNG itp.).
    """
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='medical_documents'
    )

    title = models.CharField(max_length=200)  # np. "Badanie krwi", "RTG"
    document_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='medical_docs/')

    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-document_date', '-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.animal.imie})"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    animal = models.ForeignKey("Animal", on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "animal")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.animal}"
