from rest_framework.viewsets import ModelViewSet
from pets.models import Pet, Category, Review, PetImage
from pets.serializers import PetSerializer, CategorySerializer, ReviewSerializer, PetImageSerializer
from pets.paginations import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from pets.filters import PetFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404


class PetImageViewSet(ModelViewSet):
    serializer_class = PetImageSerializer

    def get_queryset(self):
        pet_id = self.kwargs.get('pet_pk')  # assuming nested router
        return PetImage.objects.filter(pet_id=pet_id)

    def perform_create(self, serializer):
        pet_id = self.kwargs.get('pet_pk')
        pet = get_object_or_404(Pet, pk=pet_id)
        serializer.save(pet=pet)

class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PetFilter
    pagination_class = DefaultPagination
    ordering_fields = ['price']
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
        if pet_id is None:
            pet_id = self.request.data.get('pet')
        serializer.save(user=self.request.user, pet_id=pet_id)