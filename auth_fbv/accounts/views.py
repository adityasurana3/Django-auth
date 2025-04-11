from django.shortcuts import render, redirect
from .forms import RegistrationForm, PasswordResetForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .models import User
from .utils import send_activation_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm

# Create your views here.


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)
            activation_link = reverse(
                'activate', kwargs={'uidb64': uidb64, 'token': token})
            activation_url = f"{settings.SITE_DOMAIN}{activation_link}"
            subject = f'Activate your account ' + {settings.SITE_NAME}
            template = 'activation_email'
            send_activation_email(subject, template, user.email, activation_url)
            messages.success(
                request, "Registration successful, Please check you email to activate your account")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user.is_active:
            messages.warning(
                request, "This account has been already activated")
            return redirect("logon")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            messages.error("The activation link is invalid or has expired")
            return redirect('login')
    except (ValueError):
        messages.error(
            request, "The activation link is invalid or has expired")
        return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, "Both email and password is required")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_seller:
                return redirect('seller_dashboard')
            elif request.user.is_customer:
                return redirect('customer_dashboard')
            else:
                messages.error(
                    request, 'You do not have permission to access this page')
                return redirect('home')
        else:
            messages.error(request, 'Wrong email or password')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('home')


def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse(
                    'password_reset_confirm', kwargs={
                        'uidb64': uidb64, 'token': token}
                )
                absolute_reset_url = f"{request.build_absolute_uri(reset_url)}"
                subject = f"Reset your password + {settings.SITE_NAME}"
                template = 'activation_email'
                send_activation_email(subject, template, user.email, absolute_reset_url)
            messages.success(
                request, ("We have sent you a password reset link. Please check your email."))
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {"form": form})


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            messages.error(request, "Link has expired or is invalid")
            return redirect('password_reset')
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your password has been successfully reset.")
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirmation.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(
            request, "An error has occurred. Please try again later")
        return redirect('password_reset')
