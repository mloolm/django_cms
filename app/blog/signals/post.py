from django.db.models.signals import pre_save
from django.dispatch import receiver
from blog.models import Post

@receiver(pre_save, sender=Post)
def process_snipet(sender, instance, **kwargs):
    if instance.snipet:
        return

    #Формируем снипет автоматически
    instance.snipet = Post.form_snipet(instance.content)