from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_login_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile({self.user.username})"
