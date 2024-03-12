***********************
Wagtail Image Uploader
***********************

Wagtail Image Uploader is a small package to provide an easy to use API for uploading images to one or more Wagtail sites in code.
It is has two main components; a django view accepting uploads and a command-line client called `wiuc` making the uploads.

Features
--------

* Single entry point for uploading images, protected by a long-ass access key generated for each user.

Current status
--------------

* Version : 0.1.0
* Status: alpha/proof-of-concept

Tested with
------------

* Python version 3.12.2
* Django version 5.0.2
* Wagtail version 6.0.1

Installation
------------

Clone main repository:

.. code-block:: bash

    $ git clone https://github.com/weholt/wagtail-image-uploader.git
    $ cd wagtail-image-uploader
    $ pip install .

Or

.. code-block:: bash

    $ pip install git+https://github.com/weholt/wagtail-image-uploader.git

Add image uploader at the top of your installed apps:

.. code-block:: bash

    INSTALLED_APPS = [
        "image_uploader",
    ]

Add *path("", include("image_uploader.urls")),* to your urls.py.

Optionally, you can specify post-processors which process your images and metadata after they're uploaded:

.. code-block:: bash

    IMAGE_UPLOADER = {
        'POST_PROCESSORS': [
            "image_uploader.processors.post_processor.AssignTitleFromMetadataPostProcessor",
            "image_uploader.processors.post_processor.AssignTagsFromMetadataPostProcessor",
            "image_uploader.processors.post_processor.AssignCollectionFromMetadataPostProcessor"
        ]
    }

Run migrate to make sure all database migrations are applied:

.. code-block:: bash

    $ python manage.py migrate


Basic Usage
-----------

Your site is ready to accept uploads, but to use the client you'll have to do a few things;

Create superuser allowed to upload images using the API:

.. code-block:: bash

    $ python manage.py createsuperuser
    $ python manage.py get_upload_key <username>

Take note of the key printed on the screen, you'll need it later. Now create file called .image_uploader.toml in your home or current
directory. The one in the current folder will be used as standard, and the one in your home folder used as fallback.

Each site you want to upload images to gets their own section in the .image_uploader.toml file, like so:

.. code-block:: toml

    [default]
    url="http://localhost:8000/upload-image"
    api_key="<your api key for this site>"
    pre_processors=[
        # This pre-processor looks for files called filename_to_upload + .json, ie. "image_1.png.json",
        # and extracts any json data from that file and adds that date to the metadata for that specific
        # file on upload
        "image_uploader.processors.pre_processor.JsonPreProcessor",
    ]
    defaults={ 'name' = 'John', 'collections' = 'the/default/folder' } # This is added to the metadata for each file on upload

    [example]
    url="http://example.com/upload-image"
    api_key="<your api key for example.com>"

    [example2]
    url="http://example.2com/upload-image"
    api_key="<your api key for example2.com>"

The one called default is used if no site is specified. Now, from the command line you can execute the command line utility `wiuc`:

.. code-block:: bash

    $ wiuc -i test.png

And test.png in the local folder will be uploaded to the default site. To upload to several sites at once:

.. code-block:: bash

    $ wiuc -i test.png default example example2

You can also specify several files and folders to upload like so:

.. code-block:: bash

    $ wiuc -i test.png -i ./folder/with/images -i test2.png

To get more information during the process, add the --verbose flag:

.. code-block:: bash

    $ wiuc -i test.png --verbose
    ********************************************************************************

                        Wagtail Image Upload Client v.0.1.0

    ********************************************************************************
    Using .image_uploader.toml.
    Preparing to upload 1 files (2.1MiB) to 1 sites.
    Defaults: {'name': 'John'}
    Pre-processors: ['JsonPreProcessor']
    Uploading to default @ http://localhost:8000/upload-image.

    DEBUG:UploadClient for http://localhost:8000/upload-image initialized with API-key.
    DEBUG:Starting new HTTP connection (1): localhost:8000
    DEBUG:http://localhost:8000 "POST /upload-image HTTP/1.1" 201 229
    DEBUG:(Success:True) Uploaded test.png. Result: {'succes': True, 'processors': ... })
