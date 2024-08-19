from django.urls import path, include
from rest_framework import routers

from station.views import (
    TrainTypeViewSet,
    TrainViewSet,
    StationViewSet,
    RouteViewSet,
    CrewMemberViewSet,
    JourneyViewSet,
)

router = routers.DefaultRouter()
router.register("train_types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("crew_members", CrewMemberViewSet)
router.register("Journey", JourneyViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "station"
