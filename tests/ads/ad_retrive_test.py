import pytest

from ads.serializers import AdSerializer


@pytest.mark.django_db
def test_retrieve_ad(client, ad, user_token):
    response = client.get(f"/ad/{ad.pk}/",
                          content_type='application/json',
                          HTTP_AUTHORIZATION='Bearer ' + user_token
                          )

    assert response.status_code == 200
    assert response.data == AdSerializer(ad).data


@pytest.mark.django_db
def test_auth_required(client, ad):
    response = client.get(f"/ad/{ad.pk}/",
                          content_type='application/json',
                          )
    assert response.status_code == 401
