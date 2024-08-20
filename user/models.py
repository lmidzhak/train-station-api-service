from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext as _


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("email address"), unique=True)
