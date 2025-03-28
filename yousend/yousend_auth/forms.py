from django import forms
from django.forms import ModelForm

from .models import CustomUser


class LoginForm(forms.Form):
    """Form for user login."""
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


class SignupForm(ModelForm):
    """Form for user registration."""
    
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Password"}),
        }
    
    def clean_password(self):
        """Validate password (ensure strength)."""
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password
