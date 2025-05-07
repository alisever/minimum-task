import os

import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from emissions.serializers import (
    AirTravelSerializer,
    ElectricityUsageSerializer,
    PurchasedGoodsSerializer,
    detect_serializer,
)

test_directory = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.mark.parametrize(
    ("file_name", "expected_serializer", "expected_activity"),
    [
        ("air_travel.csv", AirTravelSerializer, "air_travel"),
        ("electricity.csv", ElectricityUsageSerializer, "electricity_usage"),
        ("purchased_goods_and_services.csv", PurchasedGoodsSerializer, "purchased_goods"),
    ],
)
def test_detect_serializer(file_name: str, expected_serializer: Serializer, expected_activity: str) -> None:
    file = os.path.join(test_directory, file_name)
    with open(file, "r") as f:
        header_row = f.readline().strip().split(",")
    serializer, activity = detect_serializer(header_row)
    assert serializer == expected_serializer
    assert activity == expected_activity


def test_detect_serializer_invalid() -> None:
    with pytest.raises(ValidationError, match="Unknown header row:"):
        detect_serializer(["invalid", "header", "row"])
