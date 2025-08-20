from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    breed = models.CharField(max_length=50, blank=True, null=True)
    availability = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pets')
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name or "Unnamed Pet"
    
class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')

    
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.first_name} on {self.pet.name}"