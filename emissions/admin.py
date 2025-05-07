from django.contrib import admin

from emissions.models import Emission, EmissionFactor


@admin.register(EmissionFactor)
class EmissionFactorAdmin(admin.ModelAdmin):
    list_display = ("activity", "lookup_identifiers", "unit", "co2e", "scope", "category")
    search_fields = ("lookup_identifiers",)
    filter_fields = ("activity", "scope", "category")


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    list_display = ("date", "activity", "co2e", "scope", "category", "created_at")
    search_fields = ("activity",)
    filter_fields = ("date", "activity", "scope", "category")
