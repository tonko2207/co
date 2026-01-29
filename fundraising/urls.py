from django.urls import path
from . import views

app_name = "fundraising"

urlpatterns = [
    path("", views.fundraiser_list, name="list"),
    path("create/", views.create, name="create"),
    path("<slug:slug>/", views.fundraiser_detail, name="detail"),
    path("<slug:slug>/edit/", views.fundraiser_edit, name="edit"),  # ⬅️ NOWE
]
