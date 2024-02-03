import os
import re
import uuid
from unittest.mock import patch

import pytest
from django.conf import settings
from PIL import Image, ImageFilter

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

@patch("apps.images.business_logic.Image.open", autospec=True)
@patch("apps.images.business_logic.cfutures.ProcessPoolExecutor", autospec=True)
@patch("apps.images.business_logic.cfutures.wait", autospec=True)
@pytest.mark.django_db
def test_process_image(image_open_mock, executor_mock, wait_mock, mocker):
    image = images_recipes.base_image.make()
    image_uuid_str = str(image.uuid)
    executor_mock = executor_mock.return_value.__enter__.return_value
    executor_mock.submit.return_value.result.return_value = "Testing"

    mocked_store_temporary_data = mocker.patch(
        "apps.images.business_logic.images_redis.store_temporary_data"
    )
    mocked_zip_creation_enqueue = mocker.patch(
        "apps.images.business_logic.zip_creation_enqueue"
    )

    images_business_logic.process_image(image=image)

    wait_mock.assert_called_once()
    mocked_store_temporary_data.assert_called_once_with(
        key=image_uuid_str,
        value=["Testing","Testing","Testing"] # Once per process
    )
    mocked_zip_creation_enqueue.assert_called_once_with(
        image_uuid_str=image_uuid_str
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


@pytest.mark.django_db
def test_generate_image_thumbnail(mocker):
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    PIL_image = Image.open(file_path)

    mocked_thumbnail = mocker.patch("apps.images.business_logic.Image.Image.thumbnail")
    mocked_save = mocker.patch("apps.images.business_logic.Image.Image.save")
    mocker.patch("apps.images.business_logic.create_outfile_name", return_value=file_path)

    images_business_logic.generate_image_thumbnail(img=PIL_image)

    mocked_thumbnail.assert_called_once_with((128, 128))
    mocked_save.assert_called_once_with(file_path, "PNG")


@pytest.mark.django_db
def test_generate_image_blur(mocker):
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    PIL_image = Image.open(file_path)


    mocked_filter = mocker.patch("apps.images.business_logic.Image.Image.filter")
    mocker.patch("apps.images.business_logic.create_outfile_name", return_value=file_path)

    images_business_logic.generate_image_blur(img=PIL_image)

    mocked_filter.assert_called_once_with(ImageFilter.BLUR)
    mocked_filter.return_value.save.assert_called_once_with(file_path, "PNG")


@pytest.mark.django_db
def test_generate_image_black_and_white(mocker):
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    PIL_image = Image.open(file_path)

    mocked_convert = mocker.patch("apps.images.business_logic.Image.Image.convert")
    mocker.patch("apps.images.business_logic.create_outfile_name", return_value=file_path)

    images_business_logic.generate_image_black_and_white(img=PIL_image)

    mocked_convert.assert_called_once_with("L")
    mocked_convert.return_value.save.assert_called_once_with(file_path, "PNG")
