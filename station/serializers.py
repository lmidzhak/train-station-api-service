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
    train_type = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "train_type",
            "cargo_num",
            "places_in_cargo",
            "capacity",
        )


class StationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude", "image")

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


class StationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude", "image")


class StationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "image")


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(read_only=True, slug_field="name", many=False)
    destination = serializers.SlugRelatedField(
        read_only=True, slug_field="name", many=False
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
        )


class RouteDetailSerializer(RouteListSerializer):
    source_coordinates = serializers.CharField(
        read_only=True, source="source.station_coordinates"
    )
    destination_coordinates = serializers.CharField(
        read_only=True, source="destination.station_coordinates"
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "source_coordinates",
            "destination",
            "destination_coordinates",
            "distance",
        )


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
