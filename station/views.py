from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from station.models import TrainType, Train, Station, Route, CrewMember, Journey, Order
from station.permissions import IsAdminOrIfAuthenticatedReadOnly
from station.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    StationListSerializer,
    RouteSerializer,
    CrewMemberSerializer,
    JourneySerializer,
    OrderSerializer,
    StationImageSerializer,
    StationDetailSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    CrewMemberListSerializer,
    CrewMemberDetailSerializer,
    CrewMemberImageSerializer,
)


class TrainTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class TrainViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class StationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Station.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific station"""
        station = self.get_object()
        serializer = self.get_serializer(station, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return StationImageSerializer
        if self.action == "retrieve":
            return StationDetailSerializer

        return StationListSerializer


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Route.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class CrewMemberViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CrewMember.objects.all()

    def get_serializer_class(self):
        if self.action == "upload_image":
            return CrewMemberImageSerializer
        if self.action == "list":
            return CrewMemberListSerializer
        if self.action in ["retrieve", "update"]:
            return CrewMemberDetailSerializer
        return CrewMemberSerializer

    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific crew member"""
        crew_member = self.get_object()
        serializer = self.get_serializer(crew_member, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
