from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wagtail.images import get_image_model

from .config import get_image_post_processors
from .models import ImageUploadAccessKey

Image = get_image_model()


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["file"]


@csrf_exempt
def upload_image(request):
    api_key = request.POST.get("api_key")
    if not api_key:
        return JsonResponse({"succes": False, "reason": "Missing API key"}, status=401)

    acces_key = ImageUploadAccessKey.get_user_by_key(api_key)
    if not acces_key:
        return JsonResponse({"succes": False, "reason": "User has no upload access"}, status=401)

    if not request.FILES:
        return JsonResponse({"succes": False, "reason": "Missing files"}, status=400)

    form = ImageUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse(
            {"succes": False, "reason": "Form errors", "errors": form.errors},
            status=400,
        )

    processors_applied = []
    image = form.save()
    try:
        for processor in get_image_post_processors():
            processor.process(image, request.POST)
            processors_applied.append(processor.__class__.__name__)
        image.save()
    except Exception as ex:
        return JsonResponse({"succes": False, "reason": str(ex)}, status=201)

    return JsonResponse(processors_applied and {"succes": True, "processors": processors_applied} or {"succes": True}, status=201)
