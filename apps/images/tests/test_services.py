import pytest

from apps.images.public import services
from apps.images.public.tests import baker_recipes as images_recipes


@pytest.mark.django_db
def test_handle_image_upload(valid_image, mocker):
    image_model = images_recipes.base_image.make()
    mocked_create_image_from_uploaded_file = mocker.patch(
        "apps.images.public.services.images_business_logic.create_image_from_uploaded_file",  # noqa: E501
        return_value=image_model,
    )
    mocked_process_image = mocker.patch(
        "apps.images.public.services.images_business_logic.process_image"
    )

    services.handle_image_upload(valid_image)

    mocked_create_image_from_uploaded_file.assert_called_once_with(
        file=valid_image
    )
    mocked_process_image.assert_called_once_with(image=image_model)
