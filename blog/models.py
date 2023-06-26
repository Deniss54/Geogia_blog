from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название категории')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Post(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название поста")
    content = RichTextField()
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name="URL")
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    author = models.ForeignKey(User, related_name="posts", on_delete=models.PROTECT, verbose_name="Автор")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовать")
    for_slider = models.BooleanField(default=False, verbose_name="Для слайдера")
    time_creat = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата Обновления")
    header_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Заглавное фото")
    photo_for_slider = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True,
                                         verbose_name="Фото для слайдера")

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-time_update', 'name']

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"post_slug": self.slug})
