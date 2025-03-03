from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from blog.models import SiteSettings, Social, Post
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from rs.models import ClamAVScanner, Imgr
import os
import uuid
from django.core.files.storage import FileSystemStorage

ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
SHARED_DIR = '/shared'


def make_image_safe(image, instance,sender, resave=True):
    uploaded_file = image

    # Создаем уникальное имя для файла
    file_ext = os.path.splitext(uploaded_file.name)[1]
    unique_name = f"{uuid.uuid4()}{file_ext}"

    SHARED_DIR = '/shared'

    # Используем FileSystemStorage для сохранения в общую папку
    temp_fs = FileSystemStorage(location=SHARED_DIR)
    temp_filename = temp_fs.save(unique_name, uploaded_file)  # Сохраняем в общую папку
    temp_filepath = os.path.join(SHARED_DIR, temp_filename)

    scanner = ClamAVScanner()
    res = scanner.scan_file(temp_filepath)

    if not res == 0:
        temp_fs.delete(temp_filename)
        raise ValidationError(res)


    if not resave:
        return image

    imager = Imgr()
    check = imager.rewrite_img(temp_filepath)

    res_image = None
    if check:
        with open(check, 'rb') as rewrite_file:
            res_image = ContentFile(rewrite_file.read(), name=os.path.basename(uploaded_file.name))
    temp_fs.delete(temp_filename)  # удаляем временный файл

    # Удаление старого файла
    if not instance._state.adding and hasattr(instance, 'pk'):
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            storage = old_instance.image.storage
            if storage.exists(old_instance.image.name):
                storage.delete(old_instance.image.name)

        if hasattr(sender, 'icon'):
            if old_instance.icon and old_instance.icon != instance.icon:
                storage = old_instance.icon.storage
                if storage.exists(old_instance.icon.name):
                    storage.delete(old_instance.icon.name)


    return res_image

@receiver(pre_save)
def process_icon(sender, instance, **kwargs):
    if sender not in [SiteSettings]:
        return

    if not instance.icon:
        return

    instance.icon = make_image_safe(instance.icon, instance, sender)

@receiver(pre_save)
def process_image(sender, instance, **kwargs):

    # Проверяем, относится ли вызов к нужной модели
    if sender not in [Post, SiteSettings]:
        return

    if not instance.image:
        return

    instance.image = make_image_safe(instance.image, instance, sender)


@receiver(pre_save, sender=Social)
def process_svg(sender, instance, **kwargs):
    if not instance.image:
        return

    instance.image = make_image_safe(instance.image, instance, sender, False)



@receiver(post_delete, sender=Post)
def delete_image_on_post_delete(sender, instance, **kwargs):
    if instance.image:
      storage = instance.image.storage
      if storage.exists(instance.image.name):
        storage.delete(instance.image.name)