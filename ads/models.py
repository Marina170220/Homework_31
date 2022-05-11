from django.db import models


class Ad(models.Model):

    name = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=2000, blank=True, null=True)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
