from django.db import models


class Activity(models.TextChoices):
    PERSONAL_TRAVEL = "Personal Travel"
    AIR_TRAVEL = "Air Travel"
    ELECTRICITY = "Electricity"
    PURCHASED_GOODS = "Purchased Goods and Services"


class EmissionFactor(models.Model):
    activity = models.CharField(max_length=100, choices=Activity.choices)
    lookup_identifiers = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    co2e = models.FloatField()
    scope = models.IntegerField()
    category = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity} | {self.lookup_identifiers} | {self.co2e} kg CO₂e"


class Emission(models.Model):
    date = models.DateField()
    activity = models.CharField(max_length=100, choices=Activity.choices)
    co2e = models.FloatField()
    scope = models.IntegerField()
    category = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity} - {self.date} - {self.co2e} kg CO₂e"
