from django.urls import path
from . import views

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('create/', views.animal_create, name='animal_create'),
    path('<int:pk>/edit/', views.animal_update, name='animal_update'),
    path('<int:pk>/', views.animal_detail, name='animal_detail'),
    path('<int:pk>/visits/create/', views.medical_visit_create, name='medical_visit_create'),
    path('<int:pk>/docs/', views.medical_documents_list, name='medical_documents_list'),
    path('<int:pk>/docs/add/', views.medical_document_add, name='medical_document_add'),
    path('about/', views.about_shelter, name='about_shelter'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('animals/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-animals/', views.my_animals, name='my_animals'),
    path('animal/<int:pk>/assign/', views.assign_to_me, name='assign_to_me'),


]
