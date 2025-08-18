from django.db import models

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
    image = models.ImageField(upload_to='pets/', blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Pet"
