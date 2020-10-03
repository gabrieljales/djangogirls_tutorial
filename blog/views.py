from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    # posts is a QuerySet
    posts = Post.objects.filter(published_date__lte=timezone.now()) # Filter by publication date
    return render(request, 'blog/post_list.html', {'posts':posts})