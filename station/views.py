from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.routers import Route

from station.models import TrainType, Train, Station, Route
from station.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    StationSerializer,
    RouteSerializer,
)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
