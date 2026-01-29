from django.urls import path
from . import twofa_views

urlpatterns = [
    path('setup/', twofa_views.twofa_setup, name='twofa_setup'),
    path('verify/', twofa_views.twofa_verify, name='twofa_verify'),
]
