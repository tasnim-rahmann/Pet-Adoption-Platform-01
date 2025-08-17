from django.urls import path, include
from rest_framework_nested import routers
from pets.views import PetViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', CategoryViewSet, basename='categories')

# Nasted Router
categories_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
categories_router.register('pets', PetViewSet, basename='category-pets')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls))
]