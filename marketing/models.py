from django.db import models
from django.conf import settings

class Post(models.Model):
    TYPE_CHOICES = [
        ("news", "Aktualność"),
        ("adoption_story", "Historia adopcji"),
    ]

    title = models.CharField("Tytuł", max_length=200)
    type = models.CharField("Typ", max_length=30, choices=TYPE_CHOICES, default="news")
    content = models.TextField("Treść")
    image = models.ImageField("Zdjęcie", upload_to="marketing/", blank=True, null=True)

    is_published = models.BooleanField("Opublikowane", default=True)
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marketing_posts",
        verbose_name="Autor",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
