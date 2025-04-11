from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('activate/<str:uidb64>/<str:token>', views.activate_account, name='activate'),
    path('password-reset', views.password_reset_view, name='password_reset'),
    path('password-reset/<uidb64>/<token>', views.password_reset_confirm_view, name='password_reset_confirm'),
]
