import os
from typing import Iterable

from django.utils.module_loading import import_string


def dynamic_import(import_strings: list[str]) -> Iterable[object]:
    for import_str in import_strings:
        try:
            yield import_string(import_str)
        except ImportError as ex:
            print(f"Error importing PRE/POST image uploader processor: {ex}")


def find_files(folder: str, extensions=None):
    "Finds files in a given folder, including subfolders, according to a list of file extensions"
    if not extensions:
        extensions = []
    for root, _, files in os.walk(folder):
        for file in files:
            if not extensions or os.path.splitext(file)[-1].lower() in extensions:
                yield os.path.join(root, file)


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
