import json
import logging
import os
from typing import Any, Iterable, Protocol

import requests

from .config import SUPPORTED_IMAGE_FORMATS


class UploadAbortedException(Exception):
    "Exception raised by a pre-processor to stop file from being uploaded."

    def __init__(self, pre_processor, msg):
        super().__init__()
        self.msg = msg
        self.pre_processor = pre_processor

    def __str__(self) -> str:
        return f"Upload aborted by pre-processor {self.pre_processor.__class__.__name__}: {self.msg}"


class PreProcessor(Protocol):
    "The base interface for all pre-processors"

    def process(self, filename: str, metadata: dict) -> tuple[str, dict]:
        return (filename, metadata)


class DummyPreProcessor:
    "Just an example pre-processor manipulating the metadata before the file is being uploaded."

    def process(self, filename, metadata):
        print("Dummy pre-processor", filename, metadata)
        metadata["dummy_was_here"] = True
        return (filename, metadata)


class AbortPreProcessor:
    "This is only to test the pre-processor."

    def process(self, filename, metadata):
        raise UploadAbortedException(self, "The thing that should not be")


class UploadHandler(Protocol):
    "Protocol for uploading files."

    def upload_file(self, url, filename: str, metadata: dict) -> tuple[bool, Any]:
        return (True, None)


class RequestBasedUploadHandler:
    "Upload handler using the requests library. The default."

    def upload_file(self, url, filename: str, metadata: dict) -> tuple[bool, Any]:
        with open(filename, "rb") as f:
            r = requests.post(url, data=metadata, files={"file": f}, timeout=10)
            return (r.status_code in [200, 201], json.loads(r.content))


class UploadClient:
    """
    Client for uploading images to a Wagtail site.
    """

    def __init__(self, url: str, api_key: str | None = None, verbose: bool = False, upload_handler: UploadHandler | None = None):
        self.url = url
        self.api_key = api_key
        self.pre_processors: Iterable[PreProcessor] = []
        self.defaults = {}
        self.verbse = verbose
        self.upload_handler = upload_handler or RequestBasedUploadHandler()

        if self.verbse and self.api_key:
            logging.debug(f"UploadClient for {self.url} initialized with API-key.")

    def add_pre_processors(self, *pre_processors: PreProcessor):
        self.pre_processors = pre_processors
        return self

    def add_defaults(self, **defaults):
        self.defaults = defaults
        return self

    def upload_files(self, *filenames, **kwargs) -> None:
        """
        Will try to upload a set of images and its metadata to a given url.
        """

        for filename in filenames:
            if not os.path.exists(filename):
                logging.warning(f"{filename} does not exist.")
                continue

            if os.path.splitext(filename)[-1] not in SUPPORTED_IMAGE_FORMATS:
                logging.warning(f"{filename} not supported.")
                continue

            metadata = {**self.defaults, **kwargs}
            metadata["api_key"] = self.api_key

            for processor in self.pre_processors:
                try:
                    filename, metadata = processor.process(filename, metadata)
                except UploadAbortedException as ex:
                    logging.fatal(f"Uploaded aborted by pre-processor: {ex}")
                    raise
            try:
                success, response = self.upload_handler.upload_file(self.url, filename, metadata)
                if self.verbse:
                    logging.debug(f"(Success:{success}) Uploaded {filename}. Result: {response}")
            except ConnectionError as ex:
                logging.warning(f"Error connecting to {self.url}: {ex}")
                raise
            except PermissionError as ex:
                logging.warning(f"Permission error reading {filename}: {ex}")
                raise
