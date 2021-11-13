import os
import uuid

from django.utils.deconstruct import deconstructible
from PIL import Image, ImageOps, UnidentifiedImageError


def remove_exif(image_input: str):
    try:
        original = Image.open(image_input)
    except UnidentifiedImageError:
        return None

    original = ImageOps.exif_transpose(original)

    # noinspection PyTypeChecker
    cleaned = Image.new(original.mode, original.size)
    cleaned.putdata(list(original.getdata()))

    return cleaned


# =============================================================================


@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{{{uuid.uuid4()}}}.{{{ext}}}"

        return os.path.join(self.path, filename)
