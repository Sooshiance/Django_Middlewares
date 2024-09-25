import os
from io import BytesIO

from django.utils.deprecation import MiddlewareMixin
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image


class ShellDefenderMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method == 'POST' and 'file' in request.FILES:
            file = request.FILES['file']
            if file.content_type == 'image/png':
                image = Image.open(file)
                output = BytesIO()
                image = image.convert('RGB')  # Convert to RGB
                image.save(output, format='JPEG')
                output.seek(0)
                file_name = os.path.splitext(file.name)[0] + '.jpg'
                request.FILES['file'] = InMemoryUploadedFile(
                output, 'file', file_name, 'image/jpeg', output.getbuffer().nbytes, None
                )
                response = self.get_response(request)

        return response
