import os
import sys
import tomllib
from pathlib import Path

import click

from image_uploader import __VERSION__
from image_uploader.client import UploadClient
from image_uploader.config import SUPPORTED_IMAGE_FORMATS
from image_uploader.utils import dynamic_import, find_files, sizeof_fmt


@click.command()
@click.argument("sites", nargs=-1)
@click.option("--verbose", is_flag=True, show_default=True, default=False)
@click.option("--input", "-i", "__input", multiple=True, help="Filenames or folders")
def main(__input, sites, verbose=False):
    """
    CLI for the Wagtail Image Uploader.
    """
    click.echo("*" * 80)
    click.echo("")
    click.echo(click.style(f"Wagtail Image Upload Client v.{__VERSION__}".center(80), fg="blue"))
    click.echo("")
    click.echo("*" * 80)

    local_config = os.path.join(os.getcwd(), ".image_uploader.toml")
    global_config = os.path.join(Path.home(), ".image_uploader.toml")

    if not os.path.exists(local_config) and not os.path.exists(global_config):
        click.echo(click.style(f"\n\nNo configuration found in {local_config} or {global_config}. Aborting.\n", fg="red"))
        sys.exit(1)

    config = os.path.exists(local_config) and local_config or global_config
    click.echo(click.style(f"Using {config}.", fg="green"))

    sites = sites or ["default"]

    files = []
    for value in __input:
        if os.path.isdir(value):
            files.extend(find_files(value, extensions=SUPPORTED_IMAGE_FORMATS))
        elif os.path.isfile(value):
            files.append(value)

    file_size = 0
    for filename in files:
        file_size += os.stat(filename).st_size

    if not files:
        click.echo(click.style("\n\nYou got to give files or folders to process as input using one or more -i <filename or folder>. Exiting.\n", fg="red"))
        main(["--help"])
    else:
        click.echo(click.style(f"Preparing to upload {len(files)} files ({sizeof_fmt(file_size)}) to {len(sites)} sites.", fg="green"))
        with open(config, "rb") as f:
            data = tomllib.load(f)
            for site in sites:
                api_key = data.get(site, {}).get("api_key")
                url = data.get(site, {}).get("url")
                defaults = data.get(site, {}).get("defaults", {})
                if defaults:
                    click.echo(click.style(f"Defaults: {defaults}", fg="green"))

                pre_processors = []
                pre_processors_strings = data.get(site, {}).get("pre_processors")
                if pre_processors_strings:
                    pre_processors = [p() for p in dynamic_import(pre_processors_strings)]
                    pre_processor_names = [p.__class__.__name__ for p in pre_processors]
                    click.echo(click.style(f"Pre-processors: {pre_processor_names}", fg="green"))

                click.echo(click.style(f"Uploading to {site} @ {url}.", fg="green"))
                print("")

                client = UploadClient(url, api_key, verbose)
                client.add_pre_processors(*pre_processors)
                client.add_defaults(**defaults)
                client.upload_files(*files)
