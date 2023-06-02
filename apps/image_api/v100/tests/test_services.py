from apps.image_api.v100.public import services as image_api_services


def test_handle_image_upload(mocker, valid_image):
    mocked_handle_image_upload = mocker.patch(
        "apps.image_api.v100.public.services.images_services.handle_image_upload"  # noqa: E501
    )
    image_api_services.handle_image_upload(image=valid_image)
    mocked_handle_image_upload.assert_called_once_with(image=valid_image)


def test_get_image_zipfile(mocker):
    mocked_get_image_zipfile = mocker.patch(
        "apps.image_api.v100.public.services.images_services.get_image_zipfile"
    )
    image_uuid_str = "123"
    image_api_services.get_image_zipfile(image_uuid_str=image_uuid_str)
    mocked_get_image_zipfile.assert_called_once_with(
        image_uuid_str=image_uuid_str
    )
