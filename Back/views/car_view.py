from rest_framework import viewsets, status
from Back.models.car import Car
from Back.serializers.car_serializer import CarSerializer
from Back.permissions import IsAdminOrReadOnly  
from rest_framework.response import Response

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]
