import uuid

import pytest
from django.urls import reverse
from rest_framework import status
from django.conf import settings


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


@pytest.mark.django_db
def test_image_view_set_retrieve(api_client):
    zip_data = b"Sample ZIP file data"
    pk = uuid.uuid4()
    zip_file_path = f"{settings.TMP_FILES_ROOT}{pk}.zip"
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(zip_data)

    url = reverse("image-detail", kwargs={"pk": pk})

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Type"] == "application/zip"
    assert (
        response["Content-Disposition"]
        == f'attachment; filename="{zip_file_path}"'
    )
    assert response.content == zip_data


@pytest.mark.django_db
def test_image_view_set_create_missing_file(api_client):
    url = reverse("image-list")
    data = {}

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "No image file provided!"


@pytest.mark.django_db
def test_image_view_set_create_invalid_file(api_client):
    url = reverse("image-list")
    data = {"instance": "invalid_file"}

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["instance"][0].code == "invalid"


@pytest.mark.django_db
def test_image_view_set_retrieve_invalid_uuid(api_client):
    invalid_uuid = "invalid_uuid"
    url = reverse("image-detail", kwargs={"pk": invalid_uuid})

    response = api_client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid image UUID"
