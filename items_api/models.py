from django.db import models

# Create your models here.
from django.contrib.auth.models import User

    
class Items(models.Model):
    sku = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    tags = models.TextField(max_length=500, default='Hi')
    in_stock = models.BooleanField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.sku
