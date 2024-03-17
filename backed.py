# models.py

from django.db import models

class Product(models.Model):
   name = models.CharField(max_length=255)
   description = models.TextField(null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return self.name

class ProductVariant(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
   name = models.CharField(max_length=255)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   stock = models.PositiveIntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f"{self.product.name} - {self.name}"

# serializers.py

from rest_framework import serializers
from .models import Product, ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
   class Meta:
       model = ProductVariant
       fields = ['name', 'price', 'stock']

class ProductSerializer(serializers.ModelSerializer):
   variants = ProductVariantSerializer(many=True)

   class Meta:
       model = Product
       fields = ['name', 'description', 'variants']

   def create(self, validated_data):
       variants_data = validated_data.pop('variants')
       product = Product.objects.create(**validated_data)
       for variant_data in variants_data:
           ProductVariant.objects.create(product=product, **variant_data)
       return product

# views.py

from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
   queryset = Product.objects.all()
   serializer_class = ProductSerializer

# urls.py

from django.urls import path
from .views import ProductCreateAPIView

urlpatterns = [
   path('products/create/', ProductCreateAPIView.as_view(), name='create-product'),
]