import tomllib
from typing import Iterable

from .config import PreProcessor, UploadClientConfiguration
from .utils import dynamic_import


def pre_processors_from_strings(pre_processors_strings: list[str]) -> Iterable[PreProcessor]:
    return pre_processors_strings and [p() for p in dynamic_import(pre_processors_strings)] or []  # type: ignore NOQA


def create_config_from_dict(data: dict) -> dict[str, UploadClientConfiguration]:
    result = {}
    for site in data.keys():
        api_key = data.get(site, {}).get("api_key")
        url = data.get(site, {}).get("url")
        defaults = data.get(site, {}).get("defaults", {})
        pre_processors = pre_processors_from_strings(data.get(site, {}).get("pre_processors"))
        result[site] = UploadClientConfiguration(api_key=api_key, url=url, defaults=defaults, pre_processors=pre_processors)
    return result


def create_config_from_toml(tomlfile: str) -> dict[str, UploadClientConfiguration]:
    with open(tomlfile, "rb") as f:
        return create_config_from_dict(tomllib.load(f))
