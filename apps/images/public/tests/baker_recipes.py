from model_bakery.recipe import Recipe

from apps.images.models import Image

base_image = Recipe(Image, _create_files=True)
