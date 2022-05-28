from django.db.models import Q
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, Selection
from ads.permissions import SelectionEditPermission, AdEditPermission
from ads.serializers import CategorySerializer, AdSerializer, AdCreateSerializer, AdUpdateSerializer, \
    AdDeleteSerializer, AdUploadImageSerializer, SelectionDetailSerializer, SelectionListSerializer, SelectionSerializer


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdListView(ListAPIView):
    """
    Получение списка всех объявлений.

    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):

        self.queryset = self.queryset.select_related("author", "category").order_by("-price")

        search_categories = request.GET.getlist('cat', [])
        if search_categories:
            self.queryset = self.queryset.filter(category_id__in=search_categories)

        search_text = request.GET.get('text', None)
        if search_text:
            self.queryset = self.queryset.filter(name__icontains=search_text)

        search_location = request.GET.get('location', None)
        if search_location:
            self.queryset = self.queryset.filter(author__location__name__icontains=search_location)

        min_price = int(request.GET.get('price_from', 0))
        max_price = int(request.GET.get('price_to', 0))
        price_q = None

        if min_price:
            price_q = Q(price__gte=min_price)
            if max_price:
                price_q &= Q(price__lte=max_price)

        elif max_price:
            price_q = Q(price__lte=max_price)

        if price_q is not None:
            self.queryset = self.queryset.filter(price_q)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    """
    Получение объявления по id.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    """
    Создание объявления.
    """

    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    """
    Обновление объявления.
    """

    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]



class AdDeleteView(DestroyAPIView):
    """
    Удаление объявления.
    """
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]



class AdUploadImageView(UpdateAPIView):
    """
    Загрузка картинок в объявление.
    """
    queryset = Ad.objects.all()
    serializer_class = AdUploadImageSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image', None)
        self.object.save()
        return self.update(request, *args, **kwargs)


class SelectionListView(ListAPIView):
    """
    Просмотр списка подборок.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    """
    Просмотр подборки объявлений по id.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    """
    Создание подборки объявлений.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    """
    Изменение подборки объявлений.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionEditPermission]


class SelectionDeleteView(DestroyAPIView):
    """
    Удаление подборки.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionEditPermission]
