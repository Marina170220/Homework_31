import pytest


@pytest.fixture()
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = 'user_test'
    password = 'password_test'

    django_user_model.objects.create_user(
        username=username,
        password=password,
        role='admin',
        birth_date="2000-01-01"
    )

    response = client.post(
        "/user/token/",
        {"username": username,
         "password": password},
        format='json'
    )

    return response.data["access"]
