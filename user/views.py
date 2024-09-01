from rest_framework import generics

from station.permissions import IsAdminOrIfAuthenticatedReadOnly
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_object(self):
        return self.request.user
