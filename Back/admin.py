from django.contrib import admin
from Back.models.car import Car
from Back.models.user import UserProfile
from Back.models.order import Order, OrderItem

admin.site.register(Car)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)