from django.contrib import admin
from django.urls import path
from blog.views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('search/', Search.as_view(), name='search'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('addpage/', AddPost.as_view(), name='add_post'),
    path('category/<slug:cat_slug>/', HomeListView.as_view(), name='category'),
    path('post/<slug:post_slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('author/<str:author_name><int:author_id>/', AuthorPostListView.as_view(), name='posts_by_author'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('post/update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
]