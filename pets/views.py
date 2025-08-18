from rest_framework.viewsets import ModelViewSet
from pets.models import Pet, Category
from pets.serializers import PetSerializer, CategorySerializer
from pets.paginations import DefaultPagination

class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    pagination_class = DefaultPagination
    def get_queryset(self):
        category_id = self.kwargs.get('category_pk')
        if category_id:
            return Pet.objects.filter(category_id=category_id)
        return Pet.objects.all()

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
