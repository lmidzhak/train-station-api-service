from django.core.exceptions import ValidationError
from rest_framework import serializers

from station.models import (
    TrainType,
    Train,
    Station,
    Route,
    CrewMember,
    Journey,
    Order,
    Ticket,
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "train_type",
            "places_in_cargo",
            "capacity",
        )


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")

    def validate(self, data):
        if not (-90 <= data["latitude"] <= 90):
            raise serializers.ValidationError(
                {"latitude": f"Latitude must be in the range [-90, 90]"}
            )

        if not (-180 <= data["longitude"] <= 180):
            raise serializers.ValidationError(
                {"longitude": f"Longitude must be in the range [-180, 180]"}
            )
        return data


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = ("id", "first_name", "last_name", "full_name")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "train",
            "route",
            "crew_members",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["cargo_number"],
            attrs["seat_number"],
            attrs["journey"].train,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "cargo_number", "seat_number", "journey")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at")
