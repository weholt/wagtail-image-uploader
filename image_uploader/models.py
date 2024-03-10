from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from django.utils.crypto import get_random_string
from wagtail.snippets.models import register_snippet

User = get_user_model()


def get_key():
    return get_random_string(length=512)


@register_snippet
class ImageUploadAccessKey(models.Model):
    """
    A simple user - key mapping to grant access to the upload endpoint.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    key = models.CharField(
        max_length=512,
        unique=True,
        default=get_key,
        help_text="The unique key for a given user to access the upload API",
    )

    def __str__(self) -> str:
        return f"Access key for {self.user}"

    @classmethod
    def get_key(cls, username: str) -> str:
        while True:
            try:
                obj, _ = cls.objects.get_or_create(
                    user=User.objects.get(username=username),
                    defaults={"key": get_random_string(length=512)},
                )
                return obj.key
            except IntegrityError:
                pass

    @classmethod
    def get_user_by_key(cls, key: str):
        return cls.objects.filter(key=key).first()
