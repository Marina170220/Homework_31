import pytest


@pytest.mark.django_db
def test_create_ad(client, user, category):
    expected_response = {
        "id": 1,
        "name": "test_ad_name",
        "author": user.pk,
        "price": 100,
        "description": "test_description",
        "is_published": False,
        "image": None,
        "category": category.pk,
    }

    data = {
        "name": "test_ad_name",
        "price": 100,
        "description": "test_description",
        "author": user.pk,
        "category": category.pk,
        "is_published": False
    }

    response = client.post(
        "/ad/create/",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data == expected_response
