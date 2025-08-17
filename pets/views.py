from rest_framework.viewsets import ModelViewSet
from pets.models import Pet, Category
from pets.serializers import PetSerializer, CategorySerializer

class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
