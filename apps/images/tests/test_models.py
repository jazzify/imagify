import pytest

from apps.images.models import Image
from apps.images.tests import baker_recipes as images_recipes


@pytest.mark.django_db
class TestImageModel:
    def test_image_model_create(self, valid_image):
        image = Image.objects.create(instance=valid_image)

        assert isinstance(image, Image)
        assert image.instance is not None

    def test_image_model_delete(self, valid_image):
        image = images_recipes.base_image.make(instance=valid_image)
        assert Image.objects.count() == 1

        Image.objects.get(uuid=image.uuid).delete()
        assert Image.objects.count() == 0
