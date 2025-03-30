from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_page, name="login-page"),
    path("signup", views.signup_page, name="signup-page"),
    path("logout", views.logout_page, name="logout-page")
]