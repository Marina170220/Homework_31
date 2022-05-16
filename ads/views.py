import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404

from Homework_27.settings import JSON_DUMPS_PARAM, TOTAL_ON_PAGE
from ads.models import Ad, Category
from users.models import User


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryListView(ListView):
    """
    Получение списка всех категорий.
    Return: json-файл с данными категорий объявлений.
    """
    model = Category
    category_qs = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

        response = []
        for cat in self.object_list:
            response.append({
                "id": cat.id,
                "name": cat.name,
            })

        return JsonResponse(response, safe=False, json_dumps_params=JSON_DUMPS_PARAM)


class CategoryDetailView(DetailView):
    """
    Получение категории по id.
    Return: json-файл с данными категории.
    """
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            cat = self.get_object()
        except Exception:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        }, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    """
    Создание категории.
    Return: json-файл с данными категории.
    """
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        cat = Category.objects.create(
            name=cat_data["name"]
        )

        return JsonResponse({
            "id": cat.id,
            "name": cat.name}, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    """
    Обновление категории.
    Return: json-файл с данными категории.
    """
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)
        self.object.name = cat_data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name}, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    """
    Удаление категории.
    Return: редирект на страницу со статусом "ок".
    """
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    """
    Получение списка всех объявлений.
    Return: json-файл с данными объявлений.
    """
    model = Ad
    ads_qs = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related("author", "category").order_by("-price")

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.first_name,
                "author_id": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category": ad.category.name,
                "category_id": ad.category_id,
                "image": ad.image.url if ad.image else None
            })

        response = {
            "items": ads,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params=JSON_DUMPS_PARAM)


class AdDetailView(DetailView):
    """
    Получение объявления по id.
    Return: json-файл с данными объявления.
    """
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Exception:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category.name,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        }, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    """
    Создание объявления.
    Return: json-файл с данными объявления.
    """
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, pk=ad_data["author_id"])
        category = get_object_or_404(Category, pk=ad_data["category_id"])
        iOneMore = Ad.objects.last().id + 1

        ad = Ad.objects.create(
            id=iOneMore,
            name=ad_data["name"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category=category,

        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.first_name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category.name,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None

        }, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    """
    Обновление объявления.
    Return: json-файл с данными объявления.
    """
    model = Ad
    fields = ["name", "author", "price", "description", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]

        self.object.author = get_object_or_404(User, pk=ad_data["author_id"])
        self.object.category = get_object_or_404(Category, pk=ad_data["category_id"])

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.first_name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category.name,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    """
    Удаление объявления.
    Return: редирект на страницу со статусом "ок".
    """
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    """
    Загрузка картинок в объявление.
    Return: json-файл с данными объявления.
    """
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image', None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.first_name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category.name,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, json_dumps_params=JSON_DUMPS_PARAM)
