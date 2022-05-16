import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from Homework_27.settings import JSON_DUMPS_PARAM, TOTAL_ON_PAGE
from users.models import User, Location


class UserListView(ListView):
    """
    Получение списка всех пользователей.
    Return: json-файл с данными пользователей.
    """
    model = User
    user_qs = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.prefetch_related("locations")

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all()))
            })

        response = {
            "items": users,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params=JSON_DUMPS_PARAM)


class UserDetailView(DetailView):
    """
    Получение пользователя по id.
    Return: json-файл с данными пользователя.
    """
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Exception:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all()))
        }, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    """
    Создание пользователя.
    Return: json-файл с данными пользователя.
    """
    model = User
    fields = ["username", "first_name", "last_name", "password", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
        )

        for location_name in user_data['locations']:
            location, _ = Location.objects.get_or_create(name=location_name)
            user.locations.add(location)
        self.object.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all()))
        }, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    """
    Обновление данных пользователя.
    Return: json-файл с данными пользователя.
    """
    model = User
    fields = ["username", "first_name", "last_name", "password", "role", "age", "locations"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.username = user_data["username"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.password = user_data["password"]
        self.object.age = user_data["age"]

        for location_name in user_data['locations']:
            location, _ = Location.objects.get_or_create(name=location_name)
            self.object.locations.add(location)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all()))
        }, json_dumps_params=JSON_DUMPS_PARAM)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    """
    Удаление пользователя.
    Return: редирект на страницу со статусом "ок".
    """
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=200)


class UserAdsDetailView(View):
    """
    Получение списка пользователей с количеством опубликованных пользователем объявлений.
    Return: json-файл с данными пользователей.
    """
    def get(self, request):
        user_qs = User.objects.annotate(total_ads=Count('ad'))

        paginator = Paginator(user_qs, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "location": list(user.locations.all().values_list("name", flat=True)),
                "total_ads": user.total_ads,

            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
