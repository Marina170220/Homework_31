from django.db.models import Count, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from users.serializers import *


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class UserListView(ListAPIView):
    """
    Получение списка всех пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    """
    Получение пользователя по id.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    """
    Создание пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    """
    Обновление данных пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    """
    Удаление пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer


class UsersAdsDetailView(ListAPIView):
    """
    Получение списка пользователей с количеством объявлений, опубликованных каждым пользователем.
    """
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))
    serializer_class = UserAdsDetailSerializer
