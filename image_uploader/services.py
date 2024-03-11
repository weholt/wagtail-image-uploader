import logging
import os

import requests

from .config import get_image_pre_processors, get_setting
from .processors.pre_processor import UploadAbortedException


class UploadService:
    """
    Service for uploading images to a Wagtail site.
    """

    def __init__(self, api_key: str | None = None, verbose: bool = True):
        self.api_key = api_key or get_setting("API_KEY")
        self.verbse = verbose
        if self.verbse and self.api_key:
            logging.debug("UploadService initialized with API-key.")

    def upload_file(self, url, filename, **kwargs) -> bool | None:
        """
        Will try to upload an image and its metadata to a given url.
        """
        if not os.path.exists(filename):
            logging.warning(f"{filename} does not exist.")
            return

        metadata = {**kwargs}
        metadata["api_key"] = self.api_key

        for processor in get_image_pre_processors():
            try:
                filename, metadata = processor.process(filename, metadata)
            except UploadAbortedException as ex:
                logging.fatal(f"Uploaded aborted by pre-processor: {ex}")
                raise

        try:
            with open(filename, "rb") as f:
                r = requests.post(url, data=metadata, files={"file": f}, timeout=10)
                logging.info(f"Uploaded {filename}. Result: {r.content}")
                return True
        except ConnectionError as ex:
            logging.warning(f"Error connecting to {url}: {ex}")
            raise
        except PermissionError as ex:
            logging.warning(f"Permission error reading {filename}: {ex}")
            raise


def upload_file(url: str, filename: str, **kwargs):
    "Shortcut to upload a file using the UploadService"
    return UploadService().upload_file(url, filename, **kwargs)
