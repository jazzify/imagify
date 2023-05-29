import PIL
import pytest

from apps.images import providers
from apps.images.models import Image


@pytest.mark.django_db
def test_create_image_from_uploaded_file(
    valid_image, django_assert_num_queries
):
    with django_assert_num_queries(num=1):
        image = providers.create_image_from_uploaded_file(valid_image)
        assert isinstance(image, Image)


@pytest.mark.django_db
def test_create_image_from_uploaded_file_corrupted(
    corrupted_image, django_assert_num_queries
):
    with django_assert_num_queries(num=0):
        with pytest.raises(PIL.UnidentifiedImageError):
            providers.create_image_from_uploaded_file(corrupted_image)
