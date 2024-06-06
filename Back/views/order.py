from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Back.models.order import Order, OrderItem
from Back.serializers.order_serializer import OrderSerializer
from django.conf import settings
import stripe
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = request.data.get('cart')

        # Log the received cart_items for debugging
        logger.debug(f"Received cart items: {cart_items}")

        # Vérification des items dans le panier
        for item in cart_items:
            if not all(k in item for k in ('id', 'title', 'price', 'quantity', 'image_url')):
                logger.error(f"Invalid cart item format: {item}")
                return Response({'error': 'Invalid cart item format'}, status=status.HTTP_400_BAD_REQUEST)

        # Assurez-vous que tous les prix sont des floats
        total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
        
        try:
            # Create PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),  # Stripe expects the amount in cents
                currency='usd',
                metadata={'integration_check': 'accept_a_payment'},
            )

            # Create Order
            order = Order.objects.create(user=user, total_price=total_price, payment_intent_id=intent.id)
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item['id'],
                    title=item['title'],
                    price=float(item['price']),
                    quantity=item['quantity'],
                    image_url=item['image_url']
                )

            serializer = OrderSerializer(order)
            return Response({
                'order': serializer.data,
                'client_secret': intent.client_secret
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class DeleteOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, order_id):
        user = request.user
        order = get_object_or_404(Order, id=order_id, user=user)
        
        try:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting order: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
