from ckeditor.fields import RichTextField

from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
# from django.utils.text import slugify
from slugify import slugify

from blog.models import Post, Category


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class AddPostForm(forms.ModelForm):
    slug = forms.SlugField(
        max_length=100,
        required=False,
        widget=forms.HiddenInput(),
        error_messages={
            'unique': "Пост с таким URL уже существует, измените название поста.",
        }
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Post
        fields = ['name', 'slug', 'content', 'header_photo', 'cat']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        slug = cleaned_data.get('slug')
        if name and not slug:
            cleaned_data['slug'] = slugify(name)
        return cleaned_data
