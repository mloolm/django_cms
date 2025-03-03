from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Uploader
from .models import Imgr
from django.conf import settings
import os
from django.shortcuts import render, redirect

ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt  # Отключаем CSRF для этого представления
def upload_image(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']

        # Check file type
        if uploaded_file.content_type not in ALLOWED_FILE_TYPES:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        uploader = Uploader()
        res = uploader.upload(uploaded_file)

        if not res[0]:
            return JsonResponse({'error': res[1]}, status=400)

        #Safely resave the file
        imager = Imgr()
        check = imager.rewrite_img(res[1])

        if not check:
            return JsonResponse({'error': "Bad image"}, status=400)

        return JsonResponse({'location': res[0]})

    return JsonResponse({'error': 'No file uploaded'}, status=400)

def gallery_view(request):
    uploader = Uploader()
    files = uploader.scan_directory()
    return render(request, 'gallery/gallery.html', {'files': files})

def delete_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)  # Удаляем файл из файловой системы
    return redirect('gallery')

def file_list(request):
    uploader = Uploader()
    files = uploader.scan_directory()
    file_urls = [{"value": file["url"] , "title": file["name"]} for file in files]
    return JsonResponse(file_urls, safe=False)