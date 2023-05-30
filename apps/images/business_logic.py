import os
import uuid

from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile
from PIL import Image

from apps.images import providers as images_providers
from apps.images.models import Image as ImageModel
from apps.images.public.lib.constants import Process


def create_outfile_name(process: str) -> str:
    return f"{settings.MEDIA_ROOT}{process}/{uuid.uuid4()}.{process}.jpg"


def create_image_from_uploaded_file(file: TemporaryUploadedFile) -> ImageModel:
    return images_providers.create_image_from_uploaded_file(file=file)


def process_image(image: ImageModel) -> None:
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    generate_image_thumbnail(image_path=file_path)


def generate_image_thumbnail(image_path: str) -> str:
    outfile = create_outfile_name(Process.THUMBNAIL)
    try:
        with Image.open(image_path) as img:
            img.thumbnail((128, 128))
            img.save(outfile, "JPEG")
            return outfile
    except Exception as e:
        raise e
