from django import forms
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from wagtail.images import get_image_model

from .models import ImageUploadAccessKey
from .server import get_image_post_processors

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

    user = ImageUploadAccessKey.get_user_by_key(api_key)
    if not user:
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
    image = form.save(commit=False)
    image.uploaded_by_user = user
    image.save()
    metadata = QueryDict(mutable=True)
    metadata.update(request.POST)
    applied_actions = []
    try:
        for processor_class in get_image_post_processors():
            prc = processor_class(image, metadata)
            prc.process()
            image, metadata, actions = prc.result()
            processors_applied.append(processor_class.__name__)
            applied_actions.extend(actions)
        image.save()
    except Exception as ex:
        return JsonResponse({"succes": False, "reason": str(ex)}, status=201)

    return JsonResponse({"succes": True, "processors": processors_applied, "actions": list(set(applied_actions))}, status=201)
