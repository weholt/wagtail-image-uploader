import logging
import os
from typing import Any

from django.conf import settings
from django.utils.module_loading import import_string
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)

logger = logging.getLogger("image-uploader")
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

SUPPORTED_IMAGE_FORMATS = [".jpg", ".png", ".avif", ".webp"]


def get_setting(key: str, default: Any | None = None) -> Any:
    return hasattr(settings, key) and getattr(settings, key) or os.environ.get(key, default)


def get_image_processor_post():
    if hasattr(settings, "IMAGE_UPLOADER_POST_PROCESSOR"):
        try:
            return import_string(getattr(settings, "IMAGE_UPLOADER_POST_PROCESSOR"))()
        except ImportError as ex:
            print(f"Error importing upload image post-processor: {ex}")
            return


def get_image_processor_pre():
    if hasattr(settings, "IMAGE_UPLOADER_PRE_PROCESSOR"):
        try:
            return import_string(getattr(settings, "IMAGE_UPLOADER_PRE_PROCESSOR"))()
        except ImportError as ex:
            print(f"Error importing upload image post-processor: {ex}")
            return
