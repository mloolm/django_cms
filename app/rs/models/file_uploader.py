from django.core.files.storage import FileSystemStorage
import os
from .clamav import ClamAVScanner
from django.conf import settings

class Uploader:
    def __init__(self, shared_dir='/shared'):
        self.allowed = {
            'img': ['image/jpeg', 'image/png', 'image/gif'],
            'doc': ['pdf', 'doc']
        }
        self.shared_dir = shared_dir

    def upload(self, uploaded_file, path=False):
        # Save the file to a temporary directory for verification
        temp_fs = FileSystemStorage(location=self.shared_dir)
        temp_filename = temp_fs.save(uploaded_file.name, uploaded_file)
        temp_file_path = temp_fs.path(temp_filename)  # Получаем абсолютный путь к файлу

        # Checking a file with ClamAV
        scanner = ClamAVScanner()
        file_result = scanner.scan_file(temp_file_path)

        # Delete the temporary file after checking
        os.remove(temp_file_path)

        if file_result != 0:
            return [False, file_result]

        # If the file is clean, we save it to the main storage
        if not path:
            path = settings.MEDIA_ROOT

        final_fs = FileSystemStorage(location=path)
        final_filename = final_fs.save(uploaded_file.name, uploaded_file)
        file_url = final_fs.url(final_filename)  # Получаем URL файла
        file_path = final_fs.path(final_filename)

        uid = 1000
        gid = 1000
        try:
            os.chown(file_path, uid, gid)
        except PermissionError as e:
            return [False, f"Error setting file rights: {e}"]

        return [file_url, file_path]

    def scan_directory(self, allowed = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'], directory_path = False):

        if not directory_path:
            directory_path = settings.MEDIA_ROOT

        files = []
        if os.path.exists(directory_path):
            for file_name in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file_name)
                if os.path.isfile(file_path):  # Убедимся, что это файл
                    if file_name.split('.')[-1].lower() in allowed:
                        files.append({
                            "name": file_name,
                            "path": file_path,
                            "url": f"/media/{file_name}"  # Используем MEDIA_URL
                        })
        return files
