from typing import Iterable

from django.utils.module_loading import import_string


def dynamic_import(import_strings: list[str]) -> Iterable[object]:
    for import_str in import_strings:
        try:
            yield import_string(import_str)
        except ImportError as ex:
            print(f"Error importing PRE/POST image uploader processor: {ex}")

