from rest_framework import serializers
from Back.models.car import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'brand', 'description', 'color', 'gearbox', 'engine_type', 'image']
