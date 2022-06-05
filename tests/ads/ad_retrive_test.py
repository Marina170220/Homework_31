import pytest

from ads.serializers import AdSerializer


@pytest.mark.django_db
def test_retrieve_ad(client, ad, user_token):
    response_200 = client.get(f"/ad/{ad.pk}/",
                          content_type='application/json',
                          HTTP_AUTHORIZATION='Bearer ' + user_token
                          )

    response_401 = client.get(f"/ad/{ad.pk}/",
                            content_type='application/json',
                            )

    assert response_200.status_code == 200
    assert response_200.data == AdSerializer(ad).data

    assert response_401.status_code == 401
