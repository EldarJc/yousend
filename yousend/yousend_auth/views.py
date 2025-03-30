from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .utils import UserHelper
from .forms import LoginForm, SignupForm

# Create your views here.

def login_page(request):
    """Handles user login."""
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = UserHelper.login_user(request, form.cleaned_data["email"], form.cleaned_data["password"])
        if user is not None:
            return redirect("yousend_core:index-page")

    return render(request, "yousend_auth/login.html", {
        "form": form
    })


def signup_page(request):
    """Handles user registration."""
    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        UserHelper.create_user(
            request,
            form.cleaned_data["first_name"],
            form.cleaned_data["last_name"],
            form.cleaned_data["email"],
            form.cleaned_data["password"]
        )
        return redirect("yousend_core:index-page")

    return render(request, "yousend_auth/signup.html", {
        "form": form
    })


@login_required
def logout_page(request):
    """Handles user logout."""
    logout(request)
    return redirect("yousend_core:index-page")
