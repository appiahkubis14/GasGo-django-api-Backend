# tricyclers/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tricycler, Assignment,TricyclerLocation
from .serializers import TricyclerSerializer, AssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class TricyclerListCreateView(generics.ListCreateAPIView):
    queryset = Tricycler.objects.all()
    serializer_class = TricyclerSerializer

class TricyclerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tricycler.objects.all()
    serializer_class = TricyclerSerializer

class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if not latitude or not longitude:
            return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        location, created = TricyclerLocation.objects.update_or_create(
            user=user,
            defaults={"latitude": latitude, "longitude": longitude}
        )
        return Response({"message": "Location updated successfully"}, status=status.HTTP_200_OK)


class GetLocationsView(APIView):
    def get(self, request):
        locations = TricyclerLocation.objects.all().values("user__id", "latitude", "longitude", "updated_at")
        return Response(locations, status=status.HTTP_200_OK)
