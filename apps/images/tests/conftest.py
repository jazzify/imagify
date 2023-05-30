import os
import shutil
from io import BytesIO


from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import pytest
from PIL import Image

from apps.images.public.lib.constants import Process


@pytest.fixture(scope="session")
def valid_image(
    django_db_setup, django_db_blocker
):  # django_db_setup ensures the db is ready.
    with django_db_blocker.unblock():
        im = Image.new(
            mode="RGB", size=(200, 200)
        )  # create a new image using PIL
        image_io = BytesIO()  # a BytesIO object for saving image
        im.save(image_io, "JPEG")  # save the image to image_io
        image_io.seek(0)

        image = InMemoryUploadedFile(
            image_io,
            field_name="tempfile",
            name="tempfile.jpeg",
            content_type="image/jpeg",
            size=len(image_io.getvalue()),
            charset="utf-8",
        )

    yield image


@pytest.fixture(scope="session")
def corrupted_image(django_db_blocker):
    corrupted_bytes_io = BytesIO(bytes("Invalid image data", "utf-8"))
    corrupted_bytes_io.seek(0)

    with django_db_blocker.unblock():
        corrupted_uploaded_file = InMemoryUploadedFile(
            corrupted_bytes_io, None, None, None, None, None
        )

    yield corrupted_uploaded_file


def pytest_sessionfinish():
    shutil.rmtree(f"{settings.MEDIA_ROOT}", ignore_errors=True)

    path = f"{settings.MEDIA_ROOT}/{Process.THUMBNAIL}"
    os.makedirs(path)
