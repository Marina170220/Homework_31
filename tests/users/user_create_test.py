import pytest


@pytest.mark.django_db
def test_success(client):
    data = {
        "username": "test_name",
        "password": "test123",
        "birth_date": "2000-01-01",
        "email": "testmail@test.ru",
        "locations": [1]
    }

    response = client.post(
        "/user/create/",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_wrong_domain(client):
    data = {
        "username": "test_username",
        "password": "test123",
        "birth_date": "2000-01-01",
        "email": "test@rambler.ru",
        "locations": [1]
    }

    expected_response = {
        "email": [
            "Registration from an email address in the rambler.ru domain is prohibited."
        ]
    }

    response = client.post(
        "/user/create/",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.data == expected_response


@pytest.mark.django_db
def test_wrong_age(client):
    data = {
        "username": "test_username",
        "password": "test123",
        "birth_date": "2020-01-01",
        "email": "test1@test.ru",
        "locations": [1]
    }

    expected_response = {
        "birth_date": [
            "Registration is only allowed for users over 9 years old"
        ]
    }

    response = client.post(
        "/user/create/",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.data == expected_response


@pytest.mark.django_db
def test_not_found(client):
    response = client.post(
        "/users/create/",
        content_type='application/json'
    )

    assert response.status_code == 404
