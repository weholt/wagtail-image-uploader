import logging

logger = logging.getLogger("image-uploader")
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

SUPPORTED_IMAGE_FORMATS = [".jpg", ".png", ".avif", ".webp"]
