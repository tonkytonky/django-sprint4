from django.urls import path

from .views import (
    category_posts,
    create_post,
    edit_post,
    edit_profile,
    index,
    post_detail,
    profile,
)

app_name = 'blog'


urlpatterns = [
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('profile/<str:username>/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('', index, name='index'),
]
