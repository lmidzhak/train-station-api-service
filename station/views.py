from datetime import datetime

from django.db.models import Count, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
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
    JourneyListSerializer,
    JourneyDetailSerializer,
    OrderListSerializer,
)


@extend_schema_view(
    list=extend_schema(description="Get a list of all train types"),
    create=extend_schema(description="Create new train type"),
)
class TrainTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


@extend_schema_view(
    list=extend_schema(description="Get a list of all trains"),
    create=extend_schema(description="Create new train"),
)
class TrainViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


@extend_schema_view(
    list=extend_schema(description="Get a list of all train stations"),
    create=extend_schema(description="Create new train station"),
    retrieve=extend_schema(
        description="Get info about a train station with a given id number"
    ),
    update=extend_schema(
        description="Update all info about a train station with a given id number"
    ),
    partial_update=extend_schema(
        description="Partial info update of a train station with a given id number"
    ),
)
class StationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Station.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
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


@extend_schema_view(
    list=extend_schema(description="Get a list of all routes"),
    create=extend_schema(description="Create new route"),
    retrieve=extend_schema(description="Get info about route with a given id number"),
    update=extend_schema(
        description="Update all info about route with a given id number"
    ),
    partial_update=extend_schema(
        description="Partial info update of route with a given id number"
    ),
)
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


@extend_schema_view(
    list=extend_schema(description="Get a list of all crew members"),
    create=extend_schema(description="Create new crew member"),
    retrieve=extend_schema(description="Get a crew member with given id number"),
    update=extend_schema(
        description="Update all info for a crew member with given id number"
    ),
    partial_update=extend_schema(
        description="Update partial info for a crew member with given id number"
    ),
)
class CrewMemberViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CrewMember.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return CrewMemberImageSerializer
        if self.action == "list":
            return CrewMemberListSerializer
        if self.action in ["retrieve", "update"]:
            return CrewMemberDetailSerializer
        return CrewMemberSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific crew member"""
        crew_member = self.get_object()
        serializer = self.get_serializer(crew_member, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    create=extend_schema(description="Create new journey"),
    retrieve=extend_schema(description="Get info about journey with given id number"),
    update=extend_schema(description="Update all info about journey"),
    partial_update=extend_schema(description="Partial update of info about journey"),
)
class JourneyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Journey.objects.all()
        .select_related("route", "train")
        .annotate(
            tickets_available=(
                F("train__places_in_cargo") * F("train__cargo_num") - Count("tickets")
            )
        )
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        arrival_date = self.request.query_params.get("arrival")
        departure_date = self.request.query_params.get("departure")
        destination = self.request.query_params.get("to")
        source = self.request.query_params.get("from")

        queryset = self.queryset

        if arrival_date:
            date = datetime.strptime(arrival_date, "%Y-%m-%d").date()
            queryset = queryset.filter(arrival_time__date=date)

        if departure_date:
            date = datetime.strptime(departure_date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=date)

        if destination:
            queryset = queryset.filter(route__destination__name__icontains=destination)

        if source:
            queryset = queryset.filter(route__source__name__icontains=source)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "arrival_date",
                type=OpenApiTypes.DATE,
                description="Filter by arrival date (ex. ?arrival=2024-08-28)",
            ),
            OpenApiParameter(
                "departure_date",
                type=OpenApiTypes.DATE,
                description="Filter by departure date (ex. ?departure=2024-08-24)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description="Filter by destination station (ex. ?to=Lviv or ?to=lv)",
            ),
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by source station (ex. ?from=kh or ?from=Kharkiv)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get a list of journeys"""
        return super().list(request, *args, **kwargs)


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(description="List of all orders"),
    create=extend_schema(description="Create a new order"),
    retrieve=extend_schema(description="Get an order with given id number"),
    update=extend_schema(
        description="Update all info of an order with given id number"
    ),
    partial_update=extend_schema(
        description="Partially update info of an order with given id number"
    ),
    destroy=extend_schema(description="Delete info of an order with given id number"),
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__journey__route", "tickets__journey__train"
    )
    pagination_class = OrderPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
