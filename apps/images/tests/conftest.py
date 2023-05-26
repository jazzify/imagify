import base64
import shutil
from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.images.lib import constants as images_constants


@pytest.fixture(scope="session")
def image(
    django_db_setup, django_db_blocker
):  # django_db_setup ensures the db is ready.
    TEST_IMAGE = images_constants.TEST_IMAGE_REPR.strip()

    with django_db_blocker.unblock():
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),
            field_name="tempfile",
            name="tempfile.png",
            content_type="image/png",
            size=len(TEST_IMAGE),
            charset="utf-8",
        )

    yield image

    with django_db_blocker.unblock():
        shutil.rmtree("test_data", ignore_errors=True)
