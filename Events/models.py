from django.db import models
from django import forms

# Create your models here.
class CitySearch(forms.Form):
    city = forms.CharField(max_length=100, label='Enter City')


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title