from rest_framework import serializers
from order.models import Cart, CartItem
from pets.models import Pet



class SimplePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'price']


class AddCartItemSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'pet_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        pet_id = self.validated_data['pet_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, pet_id=pet_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    
    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Product with this id ({value}) doesn't exists")
        return value
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')
    class Meta:
        model = CartItem
        fields = ['id', 'pet', 'quantity', 'total_price']
    
    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.pet.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, cart:Cart):
       return sum([item.pet.price * item.quantity for item in cart.items.all()])