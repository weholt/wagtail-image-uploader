import sys
import os
import djclick as click
import toml

from image_uploader.models import ImageUploadAccessKey
from redtoolbox.text import print_header


@click.command()
@click.argument("username")
def get_upload_key(username):
    print_header("Generating api-key for image upload service", initial_blank_lines=1)
    key = ImageUploadAccessKey.get_key(username)
    click.secho(f"Key for {username} is {key}", fg="green")
    config = os.path.join(os.getcwd(), '.image_uploader.toml')
    data = {'default': {'api_key': key, 'url': "http://localhost:8000/upload-image", 'user': username}}
    operation = "Created"
    if os.path.exists(config):
        operation = "Updated"
        data = toml.load(config)
        try:
            data.setdefault('default', {}).setdefault('api_key', key)
            if "url" not in data.get("default", {}):
                data.setdefault('default', {}).setdefault('url', "http://localhost:8000/upload-image")
            if "user" not in data.get("default", {}):
                data.setdefault('default', {}).setdefault('user', username)
        except KeyError as ex:
            print(f"Error updating {config} with new key: {ex}")
            sys.exit(1)
    try:
        with open(config, 'w') as f:
            toml.dump(data, f)
        print(f"{operation} {config} with new api-key for {username}.\n")
    except IOError as ex:
        print(f"Error writing data to {config} with new key: {ex}\n")
