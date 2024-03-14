from setuptools import setup

setup(
    entry_points={
        "console_scripts": ["wiuc=image_uploader.cli:main"],
    }
)
