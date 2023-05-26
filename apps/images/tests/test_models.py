import shutil

import pytest

from apps.images.lib import constants as images_constants
from apps.images.models import Image
from apps.images.tests import baker_recipes as images_recipes


@pytest.mark.django_db
class TestImageModel:
    def pytest_runtest_teardown(self):
        shutil.rmtree(images_constants.TEST_IMAGE_DIR, ignore_errors=True)

    @pytest.fixture(autouse=True)
    def configure_settings(self, settings):
        settings.MEDIA_ROOT = images_constants.TEST_IMAGE_DIR

    def test_image_model_create(self, image):
        image = Image.objects.create(instance=image)

        assert isinstance(image, Image)
        assert image.instance is not None

    def test_image_model_delete(self, image):
        image = images_recipes.base_image.make(instance=image)
        assert Image.objects.count() == 1

        Image.objects.get(uuid=image.uuid).delete()
        assert Image.objects.count() == 0
