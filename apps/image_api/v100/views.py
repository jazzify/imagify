from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.image_api.v100.public.services import handle_image_upload
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

        image_uuid = handle_image_upload(image=file)

        return Response(str(image_uuid), status=status.HTTP_201_CREATED)
