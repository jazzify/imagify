from django.urls import include, path

urlpatterns = [
    path("v100/", include("apps.image_api.v100.public.urls")),
]
