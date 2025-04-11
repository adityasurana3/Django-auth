from django.urls import path
from . import views

urlpatterns = [
    path('customer-dashboard', views.customer_dashboard, name='customer_dashboard'),
    path('change-password', views.change_password, name='password_change')
]
