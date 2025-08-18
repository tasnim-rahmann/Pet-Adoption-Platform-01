from rest_framework import serializers
from pets.models import Pet, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class PetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Pet
        fields = ['id', 'name', 'age', 'price', 'breed', 'availability', 'category', 'category_id', 'description', 'image']
