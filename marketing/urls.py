# marketing/urls.py
from django.urls import path
from . import views

app_name = "marketing"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("panel/", views.manage_posts, name="manage_posts"),
    path("dodaj/", views.post_create, name="post_create"),
    path("<int:pk>/edytuj/", views.post_update, name="post_update"),
    path("<int:pk>/usun/", views.post_delete, name="post_delete"),
]
