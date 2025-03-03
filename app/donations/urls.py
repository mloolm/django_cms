from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_form, name='donation_form'),
    path('success/', views.donation_success, name='donation_success'),
    path('cancel/', views.donation_cancel, name='donation_cancel'),
]