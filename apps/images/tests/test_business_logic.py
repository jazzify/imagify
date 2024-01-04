import os
import re
import uuid
from unittest.mock import patch

import pytest
from django.conf import settings
from PIL import ImageFilter

from apps.images import business_logic as images_business_logic
from apps.images.public.tests import baker_recipes as images_recipes


def test_create_outfile_name():
    process = "THUMBNAIL"
    expected_regex = rf"{settings.MEDIA_ROOT}{process}/[0-9a-f]{{8}}-[0-9a-f]{{4}}-[0-5][0-9a-f]{{3}}-[089ab][0-9a-f]{{3}}-[0-9a-f]{{12}}\.{process}\.png"  # noqa: E501

    outfile = images_business_logic.create_outfile_name(process)

    assert re.match(expected_regex, outfile)


def test_create_image_from_uploaded_file(valid_image, mocker):
    mocked_create_image_from_uploaded_file = mocker.patch(
        "apps.images.business_logic.images_providers.create_image_from_uploaded_file"  # noqa: E501
    )

    images_business_logic.create_image_from_uploaded_file(file=valid_image)
    mocked_create_image_from_uploaded_file.assert_called_once_with(
        file=valid_image
    )


@pytest.mark.django_db
def test_process_image(mocker):
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)

    mocked_generate_image_thumbnail = mocker.patch(
        "apps.images.business_logic.generate_image_thumbnail"
    )
    mocked_generate_image_blur = mocker.patch(
        "apps.images.business_logic.generate_image_blur"
    )
    mocked_store_temporary_data = mocker.patch(
        "apps.images.business_logic.images_redis.store_temporary_data"
    )
    mocked_zip_creation_enqueue = mocker.patch(
        "apps.images.business_logic.zip_creation_enqueue"
    )

    images_business_logic.process_image(image=image)

    mocked_store_temporary_data.assert_called_once()
    mocked_generate_image_thumbnail.assert_called_once_with(
        image_path=file_path
    )
    mocked_generate_image_blur.assert_called_once_with(
        image_path=file_path
    )
    mocked_zip_creation_enqueue.assert_called_once_with(
        image_uuid_str=str(image.uuid)
    )


def test_zip_creation_enqueue(mocker):
    mocked_enqueu = mocker.patch(
        "apps.images.business_logic.django_rq.enqueue"
    )
    image_uuid_str = str(uuid.uuid4())
    images_business_logic.zip_creation_enqueue(image_uuid_str=image_uuid_str)

    mocked_enqueu.assert_called_once()


@pytest.mark.parametrize(
    "file_paths",
    (
        [
            "/path/to/file1.png",
            "/path/to/file2.jpg",
            "/path/to/file3.gif",
        ],
        [],
        None,
    ),
)
def test_generate_image_zipfile(mocker, file_paths):
    image_uuid_str = str(uuid.uuid4())
    expected_zip_file_path = f"{settings.TMP_FILES_ROOT}{image_uuid_str}.zip"

    mocked_retrieve_temporary_data = mocker.patch(
        "apps.images.business_logic.images_redis.retrieve_temporary_data",
        return_value=file_paths,
    )
    mocked_write = mocker.MagicMock()
    mocked_zipfile = mocker.patch("apps.images.business_logic.zipfile.ZipFile")
    mocked_zipfile.return_value.__enter__.return_value.write = mocked_write

    images_business_logic.generate_image_zipfile(image_uuid_str=image_uuid_str)

    mocked_retrieve_temporary_data.assert_called_once_with(image_uuid_str)

    if file_paths:
        mocked_zipfile.assert_called_once_with(expected_zip_file_path, "w")
        assert mocked_write.call_count == len(file_paths)
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            mocked_write.assert_any_call(file_path, arcname=file_name)
    else:
        mocked_zipfile.assert_not_called()
        mocked_write.assert_not_called()


@patch("apps.images.business_logic.Image.open", autospec=True)
@pytest.mark.django_db
def test_generate_image_thumbnail(image_open_mock, mocker):
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    mocker.patch("apps.images.business_logic.create_outfile_name", return_value=file_path)

    images_business_logic.generate_image_thumbnail(
        image_path=file_path
    )

    image_mock = image_open_mock.return_value.__enter__.return_value
    image_mock.thumbnail.assert_called_once_with((128, 128))
    image_mock.save.assert_called_once_with(file_path, "PNG")


@patch("apps.images.business_logic.Image.open", autospec=True)
@pytest.mark.django_db
def test_generate_image_blur(image_open_mock, mocker):
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    mocker.patch("apps.images.business_logic.create_outfile_name", return_value=file_path)

    images_business_logic.generate_image_blur(
        image_path=file_path
    )
    image_mock = image_open_mock.return_value.__enter__.return_value
    image_mock.filter.assert_called_once_with(ImageFilter.BLUR)
    image_mock.filter.return_value.save.assert_called_once_with(file_path, "PNG")


@patch("apps.images.business_logic.Image.open", autospec=True)
@pytest.mark.django_db
def test_generate_image_black_and_white(image_open_mock, mocker):
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    mocker.patch("apps.images.business_logic.create_outfile_name", return_value=file_path)

    images_business_logic.generate_image_black_and_white(
        image_path=file_path
    )
    image_mock = image_open_mock.return_value.__enter__.return_value
    image_mock.convert.assert_called_once_with("L")
    image_mock.convert.return_value.save.assert_called_once_with(file_path, "PNG")
