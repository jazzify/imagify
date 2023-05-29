from django.core.files.uploadedfile import TemporaryUploadedFile
from PIL import Image as PImage
from PIL import UnidentifiedImageError

from apps.images.models import Image


def create_image_from_uploaded_file(file: TemporaryUploadedFile) -> Image:
    try:
        with PImage.open(file) as im:
            im.verify()
        return Image.objects.create(instance=file)
    except UnidentifiedImageError as e:
        raise e
    except Exception as e:
        raise e
