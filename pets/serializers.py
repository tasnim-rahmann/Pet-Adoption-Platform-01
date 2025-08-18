from rest_framework import serializers
from pets.models import Pet, Category, Review, PetImage
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class PetImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = PetImage
        fields = ['id', 'image']


class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'age', 'price', 'breed', 
            'availability', 'category', 'category_id', 
            'description', 'images'
        ]

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    pet = PetSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'pet', 'rating', 'comment']