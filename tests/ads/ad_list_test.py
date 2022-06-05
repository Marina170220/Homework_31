import pytest

from ads.serializers import AdSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ads_list(client):

    ads = AdFactory.create_batch(10)


    expected_response = {
        "count": 10,
        "next": None,
        "previous": None,
        "results": AdSerializer(ads, many=True).data
    }

    response_200 = client.get("/ad/")
    response_404 = client.get("/ads/")

    assert response_200.status_code == 200
    assert response_200.data == expected_response

    assert response_404.status_code == 404
