import pytest


@pytest.mark.django_db
def test_create_ad(client, user, category):

    expected_response_201 = {
        "id": 1,
        "name": "test_ad_name",
        "author": user.pk,
        "price": 100,
        "description": "test_description",
        "is_published": False,
        "image": None,
        "category": category.pk,
    }

    expected_response_400 = {
        "is_published": [
            "New ad can't be published."
        ],
        "name": [
            "Ensure this field has at least 10 characters."
        ],
        "price": [
            "Ensure this value is greater than or equal to 0."]}

    data_201 = {
        "name": "test_ad_name",
        "price": 100,
        "description": "test_description",
        "author": user.pk,
        "category": category.pk,
        "is_published": False
    }

    data_400 = {
        "name": "test",
        "price": -100,
        "description": "",
        "author": user.pk,
        "category": category.pk,
        "is_published": True
    }

    response_201 = client.post(
        "/ad/create/",
        data=data_201,
        content_type='application/json'
    )

    response_400 = client.post(
        "/ad/create/",
        data=data_400,
        content_type='application/json'
    )

    response_404 = client.post(
        "/ads/create/",
        data=data_201,
        content_type='application/json'
    )

    assert response_201.status_code == 201
    assert response_201.data == expected_response_201

    assert response_400.status_code == 400
    assert response_400.data == expected_response_400

    assert response_404.status_code == 404
