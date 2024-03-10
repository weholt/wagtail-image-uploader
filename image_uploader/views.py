from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wagtail.images import get_image_model

from .config import get_image_processor_post
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

    image = form.save()
    processor = get_image_processor_post()
    if processor:
        try:
            processor.process(image, request.POST)
            return JsonResponse({"succes": True, "post_processor": processor.__clas__.__name__}, status=201)
        except Exception as ex:
            return JsonResponse({"succes": False, "reason": str(ex), "post_processor": str(processor)}, status=201)

    return JsonResponse({"succes": True}, status=201)
