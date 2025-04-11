from django.shortcuts import render, redirect
from .forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login')
def customer_dashboard(request):
    return render(request, "customer/dashboard.html")


@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(
                request, "Password changed successfully. Please login with your new password")
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user, None)
    return render(request, 'customer/change_password.html', {'form': form})
