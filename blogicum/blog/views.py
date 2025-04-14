from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category

app_name = 'blog'


def get_filtered_posts(posts=Post.objects.all()):
    """Возвращает отфильтрованные посты на основе общих условий."""
    return posts.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    ordering = ['-pub_date']
    context = {'post_list': get_filtered_posts()[:5]}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    return render(request, 'blog/detail.html', {
        'post': get_object_or_404(get_filtered_posts(), pk=post_id)
    })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_filtered_posts(category.post_set.all())
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
