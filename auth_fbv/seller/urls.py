from django.urls import path
from . import views

urlpatterns = [
    path('seller-dashboard', views.seller_dashboard, name='seller_dashboard'),
]
