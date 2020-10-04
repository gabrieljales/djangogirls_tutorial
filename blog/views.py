from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    # posts is a QuerySet
    posts = Post.objects.filter(published_date__lte=timezone.now()) # Filter by publication date
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request): # Create a new post
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # We don't want to save the post right now, because we want to add the author of the post first!
            post.author = request.user # Post author
            post.published_date = timezone.now()
            post.save() # Save the post (with the author)
            return redirect('post_detail', pk=post.pk)
    else:
         form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk): # Edit a post
     post = get_object_or_404(Post, pk=pk) # Select the model to be edited
     if request.method == "POST":
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'blog/post_edit.html', {'form': form})
