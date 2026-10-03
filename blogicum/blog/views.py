from core.constants import POSTS_BY_PAGE
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .forms import PostForm, ProfileEditForm, RegistrationForm
from .models import Category, Post

User = get_user_model()


def filtered_select_posts(posts):
    return posts.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )


def get_page_obj(post_list, request):
    paginator = Paginator(post_list, POSTS_BY_PAGE)
    return paginator.get_page(request.GET.get('page'))


def index(request):
    page_obj = get_page_obj(filtered_select_posts(Post.objects), request)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(
        filtered_select_posts(Post.objects),
        id=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


@login_required
def create_post(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    page_obj = get_page_obj(filtered_select_posts(category.posts), request)
    return render(request, 'blog/category.html', {
        'page_obj': page_obj,
        'category': category
    })


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:index')
    return render(
        request, 'registration/registration_form.html', {'form': form}
    )


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    page_obj = get_page_obj(profile_user.posts.all(), request)
    context = {
        'profile': profile_user,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        instance=request.user,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})
