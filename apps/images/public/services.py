from uuid import UUID

from django.core.files.uploadedfile import TemporaryUploadedFile

from apps.images import business_logic as images_business_logic


def handle_image_upload(image: TemporaryUploadedFile) -> UUID:
    image_model = images_business_logic.create_image_from_uploaded_file(
        file=image
    )
    images_business_logic.process_image(image=image_model)
    return image_model.uuid


def get_image_zipfile(image_uuid_str: str):
    return images_business_logic.generate_image_zipfile(
        image_uuid_str=image_uuid_str
    )
