from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Consumer
from .serializers import ConsumerSerializer

class ConsumerListCreateView(APIView):
    """
    Handle GET (list all consumers) and POST (create a new consumer) requests.
    """
    def get(self, request):
        consumers = Consumer.objects.all()
        serializer = ConsumerSerializer(consumers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ConsumerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumerDetailView(APIView):
    """
    Handle GET (retrieve), PUT (update), and DELETE (remove) requests for a specific consumer.
    """
    def get(self, request, pk):
        try:
            consumer = Consumer.objects.get(pk=pk)
        except Consumer.DoesNotExist:
            return Response({"error": "Consumer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ConsumerSerializer(consumer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            consumer = Consumer.objects.get(pk=pk)
        except Consumer.DoesNotExist:
            return Response({"error": "Consumer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ConsumerSerializer(consumer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            consumer = Consumer.objects.get(pk=pk)
            consumer.delete()
            return Response({"message": "Consumer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Consumer.DoesNotExist:
            return Response({"error": "Consumer not found"}, status=status.HTTP_404_NOT_FOUND)
