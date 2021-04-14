# Django Imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Project Imports
from account.mangers import UserManager


class User(AbstractUser):
    """
    User Model
    """
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    # Give choices on user creation
    USER_ROLES = (
        ("super_admin", "Super Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    # Attributes
    email = models.EmailField(_('email_address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_role = models.CharField(max_length=16, choices=USER_ROLES)

    def __str__(self):
        return "{}".format(self.email)
