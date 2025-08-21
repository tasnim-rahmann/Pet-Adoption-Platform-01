from order.models import Cart, Order, OrderItem
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('pet').all()
            total_price = sum([item.pet.price * item.quantity for item in cart_items])
            order = Order.objects.create(user_id=user_id,total_price=total_price)
            order_items = [
                OrderItem(
                    order = order,
                    pet = item.pet,
                    price = item.pet.price,
                    quantity = item.quantity,
                    total_price = item.pet.price * item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            cart.delete()

            return order
        
    def cancel_order(order, user):
        if user.is_staff:
            order.status = Order.CANCELDED
            order.save()
            return order
        if order.user != user:
            raise PermissionDenied({"detail": "You Can Only Cancel Your Own Order"})
        
        if order.status == Order.DELIVERED:
            raise ValidationError({"detail": "You can not cancel an order that is already delivered"})
        
        order.status = Order.CANCELDED
        order.save()
        return order