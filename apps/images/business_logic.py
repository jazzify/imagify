import os
import uuid
import zipfile

import django_rq
from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile
from PIL import Image

from apps.images import providers as images_providers
from apps.images import redis as images_redis
from apps.images.models import Image as ImageModel
from apps.images.public.lib.constants import Process


def create_outfile_name(process: str) -> str:
    return f"{settings.MEDIA_ROOT}{process}/{uuid.uuid4()}.{process}.jpg"


def create_image_from_uploaded_file(file: TemporaryUploadedFile) -> ImageModel:
    return images_providers.create_image_from_uploaded_file(file=file)


def process_image(image: ImageModel) -> None:
    image_uuid_str = str(image.uuid)
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    thumbnail_outfile = generate_image_thumbnail(image_path=file_path)

    images_redis.store_temporary_data(
        image_uuid_str,
        value=[
            thumbnail_outfile,
        ],
    )
    zip_creation_enqueue(image_uuid_str=image_uuid_str)


def zip_creation_enqueue(image_uuid_str: str) -> None:
    django_rq.enqueue(generate_image_zipfile, image_uuid_str=image_uuid_str)


def generate_image_zipfile(image_uuid_str: str) -> None:
    file_paths = images_redis.retrieve_temporary_data(image_uuid_str)
    if not file_paths:
        return

    file_name = f"{settings.TMP_FILES_ROOT}{image_uuid_str}.zip"

    with zipfile.ZipFile(file_name, "w") as zipf:
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            zipf.write(file_path, arcname=file_name)


def generate_image_thumbnail(image_path: str) -> str:
    outfile = create_outfile_name(Process.THUMBNAIL)
    try:
        with Image.open(image_path) as img:
            img.thumbnail((128, 128))
            img.save(outfile, "PNG")
            return outfile
    except Exception as e:
        raise e
