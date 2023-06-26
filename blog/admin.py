from django.contrib import admin

from blog.models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'author','is_published', 'for_slider', 'time_creat']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_published', 'for_slider')
