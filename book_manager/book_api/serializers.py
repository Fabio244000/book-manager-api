from datetime import date
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50, read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=200)
    published_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    genre = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(representation['published_date'], date):
            representation['published_date'] = representation['published_date'].isoformat()
        return representation

    def create(self, validated_data):
        return Book(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.price = validated_data.get('price', instance.price)
        return instance
