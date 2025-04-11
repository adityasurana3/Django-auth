from django import forms
from accounts.models import User


class PasswordChangeForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Incorrect password")
        return old_password

    def clean(self):
        special_character = '!@#$%^&*():;""[{]}-_=+/*-'
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            self.add_error('new_password2',
                           "Password and confirm password did not match")
        if new_password1 and not any(char in special_character for char in new_password1):
            self.add_error('new_password1',
                           "Password must contains special character")
        return cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data.get('new_password1')
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user
