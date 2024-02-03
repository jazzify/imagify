import os
import uuid
import zipfile
from concurrent import futures as cfutures

import django_rq
from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile
from PIL import Image, ImageFilter

from apps.images import providers as images_providers
from apps.images import redis as images_redis
from apps.images.models import Image as ImageModel
from apps.images.public.lib.constants import Process


def create_outfile_name(process: str) -> str:
    return f"{settings.MEDIA_ROOT}{process}/{uuid.uuid4()}.{process}.png"


def create_image_from_uploaded_file(file: TemporaryUploadedFile) -> ImageModel:
    return images_providers.create_image_from_uploaded_file(file=file)


def process_image(image: ImageModel) -> None:
    image_uuid_str = str(image.uuid)
    file_path = os.path.join(settings.BASE_DIR, image.instance.path)
    
    # Execute multiple processes for the image
    with cfutures.ProcessPoolExecutor(max_workers=5) as executor, Image.open(file_path) as img:
        # Make a copy of the original image
        edit_img = img.copy()
        futures = [
            executor.submit(generate_image_thumbnail, edit_img),
            executor.submit(generate_image_blur, edit_img),
            executor.submit(generate_image_black_and_white, edit_img)
        ]
        cfutures.wait(futures)
        images_redis.store_temporary_data(
            key=image_uuid_str,
            value=[future.result() for future in futures],
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


def generate_image_thumbnail(img: Image.Image) -> str:
    outfile = create_outfile_name(Process.THUMBNAIL)
    img.thumbnail((128, 128))
    img.save(outfile, "PNG")
    return outfile


def generate_image_blur(img: Image.Image) -> str:
    outfile = create_outfile_name(Process.BLUR)
    new_img = img.filter(ImageFilter.BLUR)
    new_img.save(outfile, "PNG")
    return outfile


def generate_image_black_and_white(img: Image.Image) -> str:
    outfile = create_outfile_name(Process.BLACK_AND_WHITE)
    new_img = img.convert("L")
    new_img.save(outfile, "PNG")
    return outfile
