from rest_framework import viewsets
from Back.models.car import Car
from Back.serializers.car_serializer import CarSerializer
from Back.permissions import IsAdminOrSelf

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrSelf]
