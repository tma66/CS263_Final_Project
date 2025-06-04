from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import os

class StreamMediaFile(APIView):
    def get(self, request):
        filename = request.GET.get('filename')
        
        if not filename:
            return Response({'error': 'Filename is required'}, status=400)
        
        file_path = f'/path/to/media/{filename}'
        
        if not os.path.isfile(file_path):
            return Response({'error': 'File not found'}, status=404)
        
        response = HttpResponse(content_type='video/mp4')
        
        def chunks():
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(1024 * 1024)  # Read in 1MB chunks
                    if not data:
                        break
                    yield data
        
        response.streaming_content = chunks()
        
        return StreamingHttpResponse(response)