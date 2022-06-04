from django.contrib.auth.models import AbstractUser
from django.db import models

from Homework_27.validators import check_age


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN)
    ]

    role = models.CharField(max_length=9, choices=ROLES, default=USER)
    locations = models.ManyToManyField(Location)
    birth_date = models.DateField(validators=[check_age])
    email = models.EmailField(unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(null=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
