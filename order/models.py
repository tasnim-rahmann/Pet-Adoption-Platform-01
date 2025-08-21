from django.db import models
from users.models import User
from uuid import uuid4
from pets.models import Pet
from django.core.validators import MinValueValidator



class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"This is {self.user.first_name}'s Cart"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'pet']]

    def __str__(self):
        return f"Here is {self.quantity} {self.pet.name}'s"
    

class Order(models.Model):
    NOT_PAID = 'Not Paid'
    READY_TO_SHIP = 'Ready To Ship'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELDED = 'Canceled'
    STATUS_CHOICES = [
        (NOT_PAID, 'Not Paid'),
        (READY_TO_SHIP, 'Ready To Ship'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELDED, 'Canceled')
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_PAID)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.id} by {self.user.first_name} - {self.status}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Here is {self.quantity} {self.pet.name}'s"
