import csv
import io
from typing import Iterable, List

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from emissions.models import Emission
from emissions.serializers.activity_serializers import (
    AirTravelSerializer,
    ElectricityUsageSerializer,
    PurchasedGoodsSerializer,
)

INPUT_FILE_HEADERS: dict[str, set[str]] = {
    "air_travel": {"date", "activity", "distance travelled", "distance units", "flight range", "passenger class"},
    "electricity_usage": {"activity", "date", "country", "electricity usage", "units"},
    "purchased_goods": {"date", "activity", "supplier category", "spend", "spend units"},
}

SERIALIZER_MAP: dict[str, Serializer] = {
    "air_travel": AirTravelSerializer,
    "electricity_usage": ElectricityUsageSerializer,
    "purchased_goods": PurchasedGoodsSerializer,
}


def detect_serializer(header_row: Iterable[str]) -> tuple[Serializer, str]:
    """
    Detects the appropriate serializer and its corresponding key based on the provided
    header row.

    :param header_row: A collection of strings representing the header row of a csv file.
    :return: A tuple containing the matched serializer and its corresponding key.
    """
    headers = {h.strip().lower() for h in header_row}

    for key, expected_headers in INPUT_FILE_HEADERS.items():
        if headers == expected_headers:
            return SERIALIZER_MAP[key], key

    raise ValidationError(f"Unknown header row: {header_row}. Expected one of {INPUT_FILE_HEADERS.keys()}.")


class EmissionUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    activity_type = None
    sub_serializer = None

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise ValidationError("File must be a CSV.")
        return value

    def validate(self, attrs):
        file = attrs["file"]

        try:
            decoded_file = file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
        except UnicodeDecodeError:
            raise ValidationError("File must be UTF-8 encoded.")

        if not reader.fieldnames:
            raise ValidationError("CSV must include a header row.")

        try:
            serializer_class, activity_type = detect_serializer(reader.fieldnames)
        except ValidationError as e:
            raise ValidationError({"file": str(e)})

        self.sub_serializer = serializer_class
        self.activity_type = activity_type

        # convert field names to snake_case
        reader.fieldnames = (
            [field.lower().replace(" ", "_") for field in reader.fieldnames] if reader.fieldnames else None
        )
        rows = list(reader)
        serializer = serializer_class(data=rows, many=True)
        serializer.is_valid(raise_exception=True)
        attrs["data"] = serializer.validated_data
        return attrs

    def create(self, validated_data) -> List[Emission]:
        data = validated_data["data"]
        return self.sub_serializer(many=True).create(data)
