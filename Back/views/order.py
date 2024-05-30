from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Back.models.order import Order, OrderItem
from Back.serializers.order_serializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = request.data.get('cart')
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)

        order = Order.objects.create(user=user, total_price=total_price)
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=item['id'],
                title=item['title'],
                price=item['price'],
                quantity=item['quantity'],
                image_url=item['imageUrl']
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
