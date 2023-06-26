from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import RegisterUserForm, AddPostForm
from blog.models import Post


class HomeListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts_list'
    title = 'Название сайта'
    paginate_by = 4

    def get_queryset(self):
        queryset = super(HomeListView, self).get_queryset()
        category_slug = self.kwargs.get('cat_slug')
        return Post.objects.filter(cat__slug=category_slug,
                                   is_published=True) if category_slug else Post.objects.filter(
            is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['posts_list'][0].cat) if self.kwargs.get('cat_slug') else self.title
        context['cat_selected'] = context['posts_list'][0].cat_id if self.kwargs.get('cat_slug') else 0
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_details.html'
    slug_url_kwarg = 'post_slug'  # по умолчанию slug
    context_object_name = 'post'

    # allow_empty = False
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].name
        # context['description'] = Post.objects.get(title=context['post']).content

        return context


class Search(ListView):
    """Поиск статей"""
    paginate_by = 2
    context_object_name = 'posts_list'
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.filter(
            (Q(name__icontains=self.request.GET.get("q")) | Q(content__icontains=self.request.GET.get("q"))) & Q(
                is_published=True))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['title'] = f'Поиск: "{self.request.GET.get("q")}"'
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # тут можно вставить бота
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class AddPost(CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        print(form.instance.slug)
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/addpage.html'
    form_class = AddPostForm
    success_url = reverse_lazy('home')
    success_msg = 'Запись успешно обновлена'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_initial(self):
        initial = super().get_initial()
        post = self.get_object()
        initial['name'] = post.name
        initial['content'] = post.content
        return initial


class AuthorPostListView(ListView):
    model = Post
    template_name = 'blog/author_post_list.html'
    context_object_name = 'author_posts'
    paginate_by = 5

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return Post.objects.filter(author_id=author_id)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=pk)
