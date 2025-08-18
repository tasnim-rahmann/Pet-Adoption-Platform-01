from rest_framework.viewsets import ModelViewSet
from pets.models import Pet, Category, Review
from pets.serializers import PetSerializer, CategorySerializer, ReviewSerializer
from pets.paginations import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from pets.filters import PetFilter
from rest_framework.filters import SearchFilter, OrderingFilter


class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PetFilter
    pagination_class = DefaultPagination
    
    ordering_fields = ['price']
    ordering = ['price']
    search_fields = ['name', 'description']

    def get_queryset(self):
        category_id = self.kwargs.get('category_pk')
        if category_id:
            return Pet.objects.filter(category_id=category_id)
        return Pet.objects.all()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        pet_id = self.kwargs.get('pet_pk')
        serializer.save(user=self.request.user, pet_id=pet_id)