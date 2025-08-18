from django.contrib import admin
from pets.models import Pet, Category, Review

# Register your models here.
admin.site.register(Pet)
admin.site.register(Category)
admin.site.register(Review)
