from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("start/onboarding/", views.onboarding, name="onboarding"),
    path("start/onboarding/complete/", views.onboarding_complete, name="onboarding_complete"),
]
