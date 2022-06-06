import pytest


@pytest.mark.django_db
def test_success(client, user, category):
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


@pytest.mark.django_db
def test_wrong_price(client, user, category):
    data = {
        "name": "test1_ad_name",
        "price": -100,
        "description": "test_description",
        "author": user.pk,
        "category": category.pk,
        "is_published": False
    }

    expected_response = {
        "price": [
            "Ensure this value is greater than or equal to 0."]}

    response = client.post(
        "/ad/create/",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.data == expected_response


@pytest.mark.django_db
def test_wrong_name(client, user, category):
    data = {
        "name": "test",
        "price": 100,
        "description": "test_description",
        "author": user.pk,
        "category": category.pk,
        "is_published": False
    }

    expected_response = {

        "name": [
            "Ensure this field has at least 10 characters."
        ]
    }

    response = client.post(
        "/ad/create/",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.data == expected_response


@pytest.mark.django_db
def test_published(client, user, category):
    data = {
        "name": "test2_ad_name",
        "price": 100,
        "description": "test_description",
        "author": user.pk,
        "category": category.pk,
        "is_published": True
    }

    expected_response = {
        "is_published": [
            "New ad can't be published."
        ]
    }

    response = client.post(
        "/ad/create/",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.data == expected_response


@pytest.mark.django_db
def test_not_found(client):
    response = client.post(
        "/ads/create/",
        content_type='application/json'
    )

    assert response.status_code == 404
