import logging
from dataclasses import dataclass
from typing import Protocol, Self, TypeVar

from django.http import QueryDict

Image = TypeVar("Image")

logger = logging.getLogger("image-uploader")
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

SUPPORTED_IMAGE_FORMATS = [".jpg", ".png", ".avif", ".webp"]


class PreProcessor(Protocol):
    "The base interface for all pre-processors"

    def process(self, filename: str, metadata: dict) -> tuple[str, dict]:
        return (filename, metadata)


class PostProcessor(Protocol):
    def __init__(self, image: Image, metadata: QueryDict) -> Self:
        ...

    def process(self, *args, **kwargs) -> bool | None:
        """
        Return true if actions have been taken.
        """


@dataclass
class UploadClientConfiguration:
    api_key: str
    url: str
    defaults: dict
    pre_processors: list[PreProcessor]
