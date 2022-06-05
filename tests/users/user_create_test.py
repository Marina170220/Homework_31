import pytest


@pytest.mark.django_db
def test_create_user(client):

    expected_response_400 = {
    "email": [
        "Registration from an email address in the rambler.ru domain is prohibited."
    ],
    "birth_date": [
        "Registration is only allowed for users over 9 years old"
    ]
}

    data_201 = {
        "username": "test_name",
        "password": "test123",
        "birth_date": "2000-01-01",
        "email": "testmail@test.ru",
        "locations": [1]
    }

    data_400 = {
        "username": "test_username",
        "password": "test123",
        "birth_date": "2020-01-01",
        "email": "test@rambler.ru",
        "locations": [1]
    }

    response_201 = client.post(
        "/user/create/",
        data=data_201,
        content_type='application/json'
    )

    response_400 = client.post(
        "/user/create/",
        data=data_400,
        content_type='application/json'
    )

    response_404 = client.post(
        "/users/create/",
        data=data_201,
        content_type='application/json'
    )

    assert response_201.status_code == 201

    assert response_400.status_code == 400
    assert response_400.data == expected_response_400

    assert response_404.status_code == 404
