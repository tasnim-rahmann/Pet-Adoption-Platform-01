from django.db import models
from users.models import User
from uuid import uuid4
from pets.models import Pet
from django.core.validators import MinValueValidator, MaxValueValidator



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