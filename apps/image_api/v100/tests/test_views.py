import uuid

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_image_view_set_not_supported_get_request(api_client):
    url = reverse("image-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_image_view_set_valid_post(api_client, valid_image):
    url = reverse("image-list")
    data = {"instance": valid_image}

    response = api_client.post(url, data=data)

    assert uuid.UUID(str(response.data))
    assert response.status_code == status.HTTP_201_CREATED
