from django.urls import path, include
from rest_framework_nested import routers
from pets.views import PetViewSet, CategoryViewSet, ReviewViewSet, PetImageViewSet

# Main routers
router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', CategoryViewSet, basename='categories')

# Nested router: pets under categories
categories_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
categories_router.register('pets', PetViewSet, basename='category-pets')

# Nested router: reviews under pets
pet_router = routers.NestedDefaultRouter(router, 'pets', lookup='pet')  
pet_router.register('reviews', ReviewViewSet, basename='pet-reviews')
pet_router.register('images', PetImageViewSet, 'pet-images')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls)),
    path('', include(pet_router.urls)),
]