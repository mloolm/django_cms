from django import forms
from .models import Post, Translation
from tinymce.widgets import TinyMCE

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PostForm(BootstrapFormMixin, forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Translation
        fields = ['title', 'content']