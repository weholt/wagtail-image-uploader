from typing import Any, Iterable

from django.conf import settings

from .config import PostProcessor
from .utils import dynamic_import


def get_setting(key: str, default: Any | None = None) -> Any:
    return hasattr(settings, "IMAGE_UPLOADER") and key in settings.IMAGE_UPLOADER and settings.IMAGE_UPLOADER[key]


def get_image_post_processors() -> Iterable[PostProcessor]:
    return get_setting("POST_PROCESSORS") and [processor for processor in dynamic_import(get_setting("POST_PROCESSORS"))] or []
