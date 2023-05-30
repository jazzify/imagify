import pytest
import re
import os
from PIL import Image

from django.conf import settings

from apps.images.public.tests import baker_recipes as images_recipes

from apps.images import business_logic as images_business_logic


@pytest.mark.parametrize("process", ("THUMBNAIL", "BWFILTER", "PROCESS"))
def test_create_outfile_name(process):
    files_path = f"{settings.MEDIA_ROOT}{process}"
    uuid_regex = r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}\."  # noqa: E501
    re_path = files_path + uuid_regex + process + ".jpg"

    outfile = images_business_logic.create_outfile_name(process=process)
    assert re.match(re_path, outfile)


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

    images_business_logic.process_image(image=image)

    mocked_generate_image_thumbnail.assert_called_once_with(
        image_path=file_path
    )


@pytest.mark.django_db
def test_generate_image_thumbnail():
    image = images_recipes.base_image.make()
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)

    outfile = images_business_logic.generate_image_thumbnail(
        image_path=file_path
    )

    with Image.open(outfile) as im:
        assert im.width == 128
