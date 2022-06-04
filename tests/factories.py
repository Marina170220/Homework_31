import factory.django

from ads.models import Category, Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    birth_date = factory.Faker("date")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    price = 100
