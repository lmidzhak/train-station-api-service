from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

import train_service.settings
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
                {"latitude": "Latitude must be in the range [-90, 90]"}
            )

        if not (-180 <= data["longitude"] <= 180):
            raise serializers.ValidationError(
                {"longitude": "Longitude must be in the range [-180, 180]"}
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
    source = serializers.SlugRelatedField(
        read_only=True, slug_field="name", many=False
    )
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
        fields = ("id", "first_name", "last_name", "full_name", "image")


class CrewMemberListSerializer(CrewMemberSerializer):
    class Meta:
        model = CrewMember
        fields = ("id", "full_name")


class CrewMemberDetailSerializer(CrewMemberSerializer):
    class Meta:
        model = CrewMember
        fields = ("id", "first_name", "last_name", "full_name", "image")


class CrewMemberImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = ("id", "image")


class JourneySerializer(serializers.ModelSerializer):
    train = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    route = serializers.StringRelatedField(many=False)
    departure_time = serializers.DateTimeField(
        read_only=True, format=train_service.settings.DATETIME_FORMAT
    )
    arrival_time = serializers.DateTimeField(
        read_only=True, format=train_service.settings.DATETIME_FORMAT
    )

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


class JourneyListSerializer(JourneySerializer):
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Journey
        fields = (
            "id",
            "train",
            "route",
            "departure_time",
            "arrival_time",
            "tickets_available",
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


class TicketListSerializer(TicketSerializer):
    journey = JourneyListSerializer(many=False, read_only=True)


class TicketSeatSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = (
            "journey",
            "cargo_number",
            "seat_number",
        )


class JourneyDetailSerializer(JourneyListSerializer):
    crew_members = CrewMemberListSerializer(many=True, read_only=True)
    taken_places = TicketSeatSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "train",
            "route",
            "departure_time",
            "arrival_time",
            "crew_members",
            "taken_places",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)
    created_at = serializers.DateTimeField(
        read_only=True, format=train_service.settings.DATETIME_FORMAT
    )

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
