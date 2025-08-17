from django.urls import path, include
from rest_framework import routers
from pets.views import PetViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]
