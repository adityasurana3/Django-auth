from django import forms
from .models import User


class RegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('seller', 'Seller')
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password']

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')
            if password != confirm_password:
                self.add_error(
                    "password", "Password and confirm password did not match")
            return cleaned_data

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.get(email=email).exists():
                raise forms.ValidationError("Email already exists")
            return email


class PasswordResetForm(forms.Form):
    email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'your@example.com'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email not found please check your email")
        return email
