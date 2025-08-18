from rest_framework import serializers
from pets.models import Pet, Category, Review
from users.models import User

# -------------------
# Category Serializer
# -------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

# -------------------
# Pet Serializer
# -------------------
class PetSerializer(serializers.ModelSerializer):
    # Nested category for read
    category = CategorySerializer(read_only=True)
    # Use category_id for write
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'age', 'price', 'breed', 
            'availability', 'category', 'category_id', 
            'description', 'image'
        ]

# -------------------
# Simple User Serializer
# -------------------
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# -------------------
# Review Serializer
# -------------------
class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    pet = PetSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'pet', 'rating', 'comment']