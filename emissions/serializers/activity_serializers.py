from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from emissions.models import Activity, Emission, EmissionFactor

KILOMETRES_PER_MILE = 1.60934
CO2E_PRECISION = 6


class AirTravelSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=["%d/%m/%Y"])
    activity = serializers.ChoiceField(choices=Activity.choices)
    distance_travelled = serializers.FloatField()
    distance_units = serializers.ChoiceField(choices=["kilometres", "miles"])
    flight_range = serializers.CharField(max_length=50)
    passenger_class = serializers.CharField(max_length=50)

    def validate_activity(self, value):
        if value != Activity.AIR_TRAVEL:
            raise serializers.ValidationError(
                f"Expected activity to be '{Activity.AIR_TRAVEL}' for air travel records."
            )
        return value

    @staticmethod
    def convert_units(validated_data):
        """Convert miles to kilometres if necessary."""
        if validated_data["distance_units"] == "miles":
            validated_data["distance_units"] = "kilometres"
            validated_data["distance_travelled"] *= KILOMETRES_PER_MILE
        return validated_data

    def create(self, validated_data):
        validated_data = self.convert_units(validated_data)
        lookup_key = f"{validated_data['flight_range']}, {validated_data['passenger_class']}"
        ef = EmissionFactor.objects.filter(
            activity=validated_data["activity"],
            lookup_identifiers__iexact=lookup_key,
            unit=validated_data["distance_units"],
        ).first()
        if not ef:
            raise ValidationError(
                f"No emission factor found for {validated_data['activity']}, "
                f"{lookup_key}, {validated_data['distance_units']}"
            )

        co2e = validated_data["distance_travelled"] * ef.co2e
        return Emission.objects.create(
            date=validated_data["date"],
            activity=validated_data["activity"],
            co2e=round(co2e, CO2E_PRECISION),
            scope=ef.scope,
            category=ef.category,
        )


class ElectricityUsageSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=["%d/%m/%Y"])
    activity = serializers.ChoiceField(choices=Activity.choices)
    country = serializers.CharField(max_length=100)
    electricity_usage = serializers.FloatField()
    units = serializers.CharField(max_length=20)

    def validate_activity(self, value):
        if value != Activity.ELECTRICITY:
            raise serializers.ValidationError(
                f"Expected activity to be '{Activity.ELECTRICITY}' for electricity usage records."
            )
        return value

    def create(self, validated_data):
        ef = EmissionFactor.objects.filter(
            activity=validated_data["activity"],
            lookup_identifiers__iexact=validated_data["country"],
            unit=validated_data["units"],
        ).first()
        if not ef:
            raise ValidationError(
                f"No emission factor found for {validated_data['activity']}, "
                f"{validated_data['country']}, {validated_data['units']}"
            )

        co2e = validated_data["electricity_usage"] * ef.co2e
        return Emission.objects.create(
            date=validated_data["date"],
            activity=validated_data["activity"],
            co2e=round(co2e, CO2E_PRECISION),
            scope=ef.scope,
            category=ef.category,
        )


class PurchasedGoodsSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=["%d/%m/%Y"])
    activity = serializers.ChoiceField(choices=Activity.choices)
    supplier_category = serializers.CharField(max_length=100)
    spend = serializers.FloatField()
    spend_units = serializers.CharField(max_length=20)

    def validate_activity(self, value):
        if value != Activity.PURCHASED_GOODS:
            raise serializers.ValidationError(
                f"Expected activity to be '{Activity.PURCHASED_GOODS}' for purchased goods records."
            )
        return value

    def create(self, validated_data):
        ef = EmissionFactor.objects.filter(
            activity=validated_data["activity"],
            lookup_identifiers__iexact=validated_data["supplier_category"],
            unit=validated_data["spend_units"],
        ).first()
        if not ef:
            raise ValidationError(
                f"No emission factor found for {validated_data['activity']}, "
                f"{validated_data['supplier_category']}, {validated_data['spend_units']}"
            )

        co2e = validated_data["spend"] * ef.co2e
        return Emission.objects.create(
            date=validated_data["date"],
            activity=validated_data["activity"],
            co2e=round(co2e, CO2E_PRECISION),
            scope=ef.scope,
            category=ef.category,
        )
