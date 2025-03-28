from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """Custom user model that uses email as the username."""
    
    # Disabling the default username field
    username = None

    # Using email as the unique identifier for the user
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """String representation of the user (full name)."""
        return f"{self.first_name} {self.last_name}"

    # Specifying the custom field for login
    USERNAME_FIELD = "email"
    
    # Required fields during user creation via the admin
    REQUIRED_FIELDS = ["first_name", "last_name"]
