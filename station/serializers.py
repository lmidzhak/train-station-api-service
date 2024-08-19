from rest_framework import serializers

from station.models import TrainType, Train


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
