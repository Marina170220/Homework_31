from rest_framework import serializers

from ads.models import Category, Ad
from users.serializers import LocationSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(max_length=20)
    category_name = serializers.CharField(max_length=20)
    location = LocationSerializer(many=True)

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author_name', 'price', 'description', 'is_published', 'image', 'category_name',
                  'location']


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']


class AdUploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['image']
