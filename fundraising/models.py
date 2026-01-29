from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Fundraiser(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(verbose_name="Opis")
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Cel (PLN)")
    collected_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Zebrano (PLN)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktywna")
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True, verbose_name="Koniec zbiórki (opcjonalnie)")

    class Meta:
        verbose_name = "Zbiórka"
        verbose_name_plural = "Zbiórki"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while Fundraiser.objects.filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_ended(self):
        return self.ends_at is not None and self.ends_at < timezone.now()


class Donation(models.Model):
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Kwota (PLN)")
    donor_name = models.CharField(max_length=120, blank=True, verbose_name="Imie (opcjonalnie)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wpłata"
        verbose_name_plural = "Wpłaty"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.fundraiser.title} - {self.amount} PLN"
