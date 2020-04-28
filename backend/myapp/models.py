from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    confirmed = models.PositiveIntegerField()
    active = models.PositiveIntegerField()
    recovered = models.PositiveIntegerField()
    deceased = models.PositiveIntegerField()
    latitude = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    last_update = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    confirmed = models.PositiveIntegerField()
    active = models.PositiveIntegerField()
    recovered = models.PositiveIntegerField()
    deceased = models.PositiveIntegerField()
    latitude = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    last_update = models.DateTimeField()
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    confirmed = models.PositiveIntegerField()
    latitude = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    last_update = models.DateTimeField()
    def __str__(self):
        return self.name