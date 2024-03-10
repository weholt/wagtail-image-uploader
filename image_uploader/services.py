import logging
import os

import requests

from .config import get_image_processor_pre, get_setting


class UploadService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or get_setting("IMAGE_UPLOADER_API_KEY")

    def upload_file(self, url, filename):
        """
        Will try to upload an image and its metadata to a given url.
        """
        if not os.path.exists(filename):
            return

        msg = None
        lg = None
        try:
            metadata = {}
            metadata["api_key"] = self.api_key

            processor = get_image_processor_pre()
            if processor:
                filename, metadata = processor.process(filename, metadata)

            try:
                with open(filename, "rb") as f:
                    r = requests.post(url, data=metadata, files={"file": f}, timeout=10)
                    msg = f"Uploaded {filename}. Result: {r.content}"
                    lg = logging.info
            except ConnectionError as ex:
                msg = f"Error connecting to {url}: {ex}"
                lg = logging.warning
            except PermissionError as ex:
                msg = f"Permission error reading {filename}: {ex}"
                lg = logging.warning
        except Exception as ex:
            msg = f"Error processing {filename}: {ex}"

        if msg and lg:
            lg(msg)
        return msg
