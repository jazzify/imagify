import uuid
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponse
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.image_api.v100.public import services as image_api_services
from apps.image_api.v100.serializers import ImageSerializer


class ImageViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin
):
    serializer_class = ImageSerializer

    def create(self, request):
        file = request.data.get("instance")
        if not file:
            return Response(
                {"error": "No image file provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_uuid = image_api_services.handle_image_upload(image=file)

        return Response(str(image_uuid), status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            uuid.UUID(pk)
        except ValueError:
            return Response(
                {"error": "Invalid image UUID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_name = f"{settings.TMP_FILES_ROOT}{pk}.zip"
        zip_file = open(file_name, "rb")

        response = HttpResponse(
            FileWrapper(zip_file), content_type="application/zip"
        )
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response
