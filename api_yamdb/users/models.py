from django.contrib.auth.models import AbstractUser
from django.db import models


USER = "user"
ADMIN = "admin"
MODERATOR = "moderator"

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, blank=False, null=False
    )
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False
    )
    first_name = models.CharField("имя", max_length=150, blank=True)
    last_name = models.CharField("фамилия", max_length=150, blank=True)
    bio = models.TextField(
        "Biography",
        blank=True,
    )
    role = models.CharField(
        "role", max_length=20, choices=ROLE_CHOICES, default=USER, blank=True
    )
    confirmation_code = models.CharField(
        "confirmation_code",
        max_length=255,
        null=True,
        blank=False,
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
