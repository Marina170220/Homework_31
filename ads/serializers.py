from rest_framework import serializers

from ads.models import Category, Ad, Selection
from Homework_27.validators import NewAdValidator
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
    is_published = serializers.BooleanField(validators=[NewAdValidator()])

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


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)
    owner = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'
