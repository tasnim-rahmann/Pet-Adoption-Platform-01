from django.contrib import admin
from pets.models import Pet, Category, Review, PetImage

# Register your models here.
admin.site.register(Pet)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(PetImage)