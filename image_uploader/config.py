import logging
from typing import Any

from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger("image-uploader")
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

SUPPORTED_IMAGE_FORMATS = [".jpg", ".png", ".avif", ".webp"]


def get_setting(key: str, default: Any | None = None) -> Any:
    return hasattr(settings, "IMAGE_UPLOADER") and key in settings.IMAGE_UPLOADER and settings.IMAGE_UPLOADER[key]


def dynamic_import(import_strings: list[str]):
    for import_str in import_strings:
        try:
            yield import_string(import_str)
        except ImportError as ex:
            print(f"Error importing PRE/POST image uploader processor: {ex}")


def get_image_pre_processors():
    return get_setting("PRE_PROCESSORS") and [processor() for processor in dynamic_import(get_setting("PRE_PROCESSORS"))] or []


def get_image_post_processors():
    return get_setting("POST_PROCESSORS") and [processor() for processor in dynamic_import(get_setting("POST_PROCESSORS"))] or []
