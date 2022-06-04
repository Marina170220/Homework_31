from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from rest_framework import serializers

from Homework_27.settings import MIN_USERS_AGE


def check_age(value: date):
    users_age = relativedelta(date.today(), value).years
    if users_age < MIN_USERS_AGE:
        raise ValidationError(f"Registration is only allowed for users over {MIN_USERS_AGE} years old")


class NewAdValidator:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError("New ad can't be published.")


class EmailCheck:
    def __init__(self, domain):
        self.domain = domain

    def __call__(self, value):
        if value.endswith(self.domain):
            raise serializers.ValidationError(
                "Registration from an email address in the rambler.ru domain is prohibited.")
