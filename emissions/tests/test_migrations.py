import pytest

from emissions.models import EmissionFactor


@pytest.mark.django_db
def test_emission_factors_csv_loads_correctly():
    assert EmissionFactor.objects.count() == 101
    emission_factor = EmissionFactor.objects.get(activity="Personal Travel", lookup_identifiers="Taxi")
    assert emission_factor.co2e == 0.937
