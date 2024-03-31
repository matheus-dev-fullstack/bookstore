from rest_framework import serializers

from product.models.product import Product, Category
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    categories_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, many=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'active',
            'category',
            'categories_id',
        ]
    
    def create(self, validated_data):
        category_ids = validated_data.pop('categories_id')
        
        product = Product.objects.create(**validated_data)
        for category_id in category_ids:
            product.category.add(category_id)
            
        return product