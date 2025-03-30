from django.contrib.auth import authenticate, login
from .models import CustomUser


class UserHelper:
    """Helper class for handling user authentication and registration."""

    @staticmethod
    def get_user_by_email(email):
        """Get user by email."""
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def login_user(request, email, password):
        """Authenticate and login user using email and password."""
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user=user)
            return user
        return None

    @staticmethod
    def create_user(request, first_name, last_name, email, password):
        """Create a new user and automatically log them in."""
        # Check if user already exists
        if UserHelper.get_user_by_email(email=email):
            return None
        
        # Create a new user
        user = CustomUser(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()

        # Log in the newly created user
        UserHelper.login_user(request, email, password)
        return user

