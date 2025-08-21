from rest_framework import serializers
from order.models import Cart, CartItem, Order, OrderItem
from pets.models import Pet
from order.services import OrderService


class EmptySerializer(serializers.Serializer):
    pass

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
        read_only_fields = ['user']

    def get_total_price(self, cart: Cart):
        return sum([item.pet.price * item.quantity for item in cart.items.all()])

    def validate(self, attrs):
        user = self.context['request'].user
        if Cart.objects.filter(user=user).exists():
            raise serializers.ValidationError("This user already has a cart.")
        return attrs
    

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id):
            raise serializers.ValidationError("No Cart Found!")
        if not CartItem.objects.filter(cart_id=cart_id):
            raise serializers.ValidationError("Cart is Empty!")
        return cart_id
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']

        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'pet', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'status', 'total_price', 'created_at']