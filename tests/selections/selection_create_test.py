import pytest


@pytest.mark.django_db
def test_create_selection(client, user, ad, user_token):
    expected_response = {
        "id": 1,
        "name": "test_selection",
        "owner": user.pk,
        "items": [ad.pk]
    }

    data = {
        "name": "test_selection",
        "owner": user.pk,
        "items": [ad.pk]
    }

    response_201 = client.post(
        "/selection/create/",
        data=data,
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + user_token
    )

    response_401 = client.post(
        "/selection/create/",
        data=data,
        content_type='application/json',
    )

    assert response_201.status_code == 201
    assert response_201.data == expected_response

    assert response_401.status_code == 401
