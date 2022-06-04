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

    response = client.get("/ad/")
    assert response.status_code == 200
    assert response.data == expected_response
