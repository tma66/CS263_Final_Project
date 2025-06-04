from django.http import FileResponse, Http404
from django.views.decorators.http import require_http_methods
import os

@require_http_methods(["GET"])
def stream_media(request, filename):
    file_path = os.path.join('media', filename)
    if not os.path.exists(file_path):
        raise Http404("File does not exist")
    response = FileResponse(open(file_path, 'rb'))
    return response