from django import template
from blog.models import Category, Post

register = template.Library()


@register.simple_tag()  # для перебора категорий
def get_categories():
    return Category.objects.all()

@register.simple_tag()  # для перебора категорий
def get_post_for_slider():
    return Post.objects.filter(is_published=True, for_slider=True)