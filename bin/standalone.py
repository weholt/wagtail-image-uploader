import os
import sys

import django
from django.conf import settings

settings.configure(
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    ALLOWED_HOSTS=["*"],  # Disable host header validation
    ROOT_URLCONF=__name__,
    SECRET_KEY=os.environ.get("SECRET_KEY", "a-bad-secret"),
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}],
    MIDDLEWARE_CLASSES=(
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
)


def configure_django_environ():
    "Configures the django environment based on the location of the manage.py file."

    try:
        from django.core.management import execute_from_command_line  # NOQA
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and " "available on your PYTHONPATH environment variable? Did you " "forget to activate a virtual environment?"
        ) from exc

    django.setup()


if __name__ == "__main__":
    configure_django_environ()
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
