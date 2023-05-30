from uuid import UUID

from django.core.files.uploadedfile import TemporaryUploadedFile

from apps.images.public import services as images_services


def handle_image_upload(image: TemporaryUploadedFile) -> UUID:
    return images_services.handle_image_upload(image=image)
