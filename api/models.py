from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    company_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.IntegerField()
    email = models.CharField(max_length=100, unique=True)
    web = models.CharField(max_length=150)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
