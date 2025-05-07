import csv
import os

from django.db import migrations


def load_emission_factors(apps, schema_editor):
    EmissionFactor = apps.get_model("emissions", "EmissionFactor")
    csv_path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "emission_factors.csv")

    emission_factors = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        emission_factors.append(
            EmissionFactor(
                activity=row["Activity"],
                lookup_identifiers=row["Lookup identifiers"],
                unit=row["Unit"],
                co2e=float(row["CO2e"]),
                scope=int(row["Scope"]),
                category=int(row["Category"]) if row["Category"] else None,
            )
        )

    EmissionFactor.objects.bulk_create(emission_factors)


class Migration(migrations.Migration):
    dependencies = [
        ("emissions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_emission_factors, atomic=False),
    ]
