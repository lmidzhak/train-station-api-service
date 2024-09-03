import os
import tempfile
from datetime import datetime

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Station, Route, TrainType, Train, Journey, CrewMember
from station.serializers import (
    JourneyListSerializer,
    RouteListSerializer,
    CrewMemberListSerializer,
)

STATION_URL = reverse("station:station-list")
JOURNEY_URL = reverse("station:journey-list")
ROUTE_URL = reverse("station:route-list")
CREW_MEMBER_URL = reverse("station:crewmember-list")


def sample_train_type(**params):
    defaults = {"name": "sleeper"}
    defaults.update(params)
    return TrainType.objects.create(**defaults)


def sample_train(**params):
    train_type = sample_train_type()
    defaults = {
        "name": "Intercity1",
        "cargo_num": 10,
        "places_in_cargo": 36,
        "train_type": train_type,
    }
    defaults.update(params)
    return Train.objects.create(**defaults)


def sample_station(**params):
    defaults = {
        "name": "Teststation",
    }
    defaults.update(params)
    return Station.objects.create(**defaults)


def sample_route(**params):
    defaults = {"distance": 500}
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_crew_member(**params):
    defaults = {
        "first_name": "John",
        "last_name": "Doe",
    }
    defaults.update(params)
    return CrewMember.objects.create(**defaults)


def sample_journey(**params):
    crew_member = sample_crew_member()
    defaults = {
        "departure_time": datetime(2024, 8, 31, 10, 0),
        "arrival_time": datetime(2024, 8, 31, 23, 0),
    }
    defaults.update(params)
    instance = Journey.objects.create(**defaults)
    instance.crew_members.add(crew_member)
    return instance


def station_image_upload_url(station_id):
    """Return URL for station image upload"""
    return reverse("station:station-upload-image", args=[station_id])


def crew_member_image_upload_url(crew_member_id):
    """Return URL for crew member image upload"""
    return reverse("station:crewmember-upload-image", args=[crew_member_id])


def station_detail_url(station_id):
    return reverse("station:station-detail", args=[station_id])


def crew_member_detail_url(crew_member_id):
    return reverse("station:crewmember-detail", args=[crew_member_id])


class StationImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@station.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.station = sample_station()

    def tearDown(self):
        self.station.image.delete()

    def test_upload_image_to_station(self):
        """Test uploading an image to station"""
        url = station_image_upload_url(self.station.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.station.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.station.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = station_image_upload_url(self.station.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_station_list(self):
        url = STATION_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {
                    "name": "Name",
                    "latitude": 10,
                    "longitude": 10,
                },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        station = Station.objects.get(name="Name")
        self.assertFalse(station.image)

    def test_image_url_is_shown_on_station_detail(self):
        url = station_image_upload_url(self.station.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(station_detail_url(self.station.id))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_station_list(self):
        url = station_image_upload_url(self.station.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(STATION_URL)

        self.assertIn("image", res.data[0].keys())


class CrewMemberImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@station.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.crew_member = sample_crew_member()

    def tearDown(self):
        self.crew_member.image.delete()

    def test_upload_image_to_crew_member(self):
        """Test uploading an image to crew member"""
        url = crew_member_image_upload_url(self.crew_member.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.crew_member.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.crew_member.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = crew_member_image_upload_url(self.crew_member.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_crew_member_list(self):
        url = CREW_MEMBER_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {"first_name": "Jane", "last_name": "Doe"},
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        crew_member = CrewMember.objects.get(first_name="Jane", last_name="Doe")
        self.assertFalse(crew_member.image)

    def test_image_url_is_shown_on_crew_member_detail(self):
        url = crew_member_image_upload_url(self.crew_member.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(crew_member_detail_url(self.crew_member.id))

        self.assertIn("image", res.data)


class UnauthenticatedJourneyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(JOURNEY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedJourneyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "testpass")
        self.station1 = sample_station(name="Lviv")
        self.station2 = sample_station(name="Kyiv")
        self.train_type1 = sample_train_type(name="sleeper")
        self.train = sample_train(
            name="Intercity",
            cargo_num=10,
            places_in_cargo=36,
            train_type=self.train_type1,
        )

        self.route1 = sample_route(source=self.station1, destination=self.station2)
        self.route2 = sample_route(source=self.station2, destination=self.station1)
        self.journey1 = sample_journey(
            route=self.route1,
            departure_time=datetime(2024, 8, 11, 10, 0),
            arrival_time=datetime(2024, 8, 11, 20, 0),
            train=self.train,
        )
        self.journey2 = sample_journey(
            route=self.route2,
            departure_time=datetime(2024, 8, 12, 10, 0),
            arrival_time=datetime(2024, 8, 12, 20, 0),
            train=self.train,
        )

        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        res = self.client.get(ROUTE_URL)
        routes = Route.objects.order_by("id")
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_crew_members(self):
        res = self.client.get(CREW_MEMBER_URL)
        routes = CrewMember.objects.order_by("id")
        serializer = CrewMemberListSerializer(routes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_journeys(self):

        res = self.client.get(JOURNEY_URL)

        journeys = Journey.objects.order_by("id")
        serializer = JourneyListSerializer(journeys, many=True)

        expected_data = serializer.data
        for journey in expected_data:
            journey["tickets_available"] = 360

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_filter_journey_by_route_source(self):
        res1 = self.client.get(JOURNEY_URL, {"from": "lv"})
        serializer1 = JourneyListSerializer(self.journey1)
        serializer1_data = serializer1.data

        serializer1_data["tickets_available"] = 360
        self.assertIn(serializer1_data, res1.data)

    def test_filter_journey_by_route_destination(self):
        res2 = self.client.get(JOURNEY_URL, {"to": "lv"})
        serializer2 = JourneyListSerializer(self.journey2)
        serializer2_data = serializer2.data

        serializer2_data["tickets_available"] = 360
        self.assertIn(serializer2_data, res2.data)

    def test_filter_journey_by_departure_time(self):
        res = self.client.get(JOURNEY_URL, {"departure": "2024-08-11"})

        serializer1 = JourneyListSerializer(self.journey1)
        serializer1_data = serializer1.data
        serializer1_data["tickets_available"] = 360

        self.assertIn(serializer1_data, res.data)

    def test_filter_journey_by_arrival_time(self):
        res = self.client.get(JOURNEY_URL, {"arrival": "2024-08-12"})

        serializer1 = JourneyListSerializer(self.journey2)
        serializer1_data = serializer1.data
        serializer1_data["tickets_available"] = 360

        self.assertIn(serializer1_data, res.data)
