from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

PHONE_NUMBER_VALIDATOR = RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'Invalid Phone Number!')


class Contact(models.Model):
    company_name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, validators=[PHONE_NUMBER_VALIDATOR])
    location = models.CharField(max_length=255, blank=True, null=True)
    personal_name = models.CharField(max_length=255, blank=True, null=True)
    personal_phone = models.CharField(max_length=255, blank=True, null=True, validators=[PHONE_NUMBER_VALIDATOR])
    service_type = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(default=0)
    situation = models.CharField(max_length=255, null=True, blank=True)
    date_of_meeting = models.DateTimeField(null=True, blank=True)
    owned_by = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    Created = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    latitude = models.DecimalField(default=0, decimal_places=10, max_digits=15)
    longitude = models.DecimalField(default=0, decimal_places=10, max_digits=15)

    def __str__(self):
        return str(f"{self.company_name},Situation:{self.situation}")


class Costumer(models.Model):
    name = models.TextField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    latitude = models.DecimalField(default=0, decimal_places=10, max_digits=15)
    longitude = models.DecimalField(default=0, decimal_places=10, max_digits=15)

    def __str__(self):
        return str(f"{self.name}")
