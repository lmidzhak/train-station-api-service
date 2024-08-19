from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.routers import Route

from station.models import TrainType, Train, Station
from station.serializers import TrainTypeSerializer, TrainSerializer, StationSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
