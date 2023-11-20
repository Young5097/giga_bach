from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def board(request):
<<<<<<< HEAD
    posts = posts = Post.objects.all().order_by('-created_at')
    return render(request, "board.html", {"posts": posts})
=======
    posts = Post.objects.all()
    return render(request, "board.html", {"posts": posts, "user": request.user})
>>>>>>> eeb6e9f7fb30e90dea0759d077c4b75b2f9bc960


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("board")  # 게시글 목록 페이지로 이동
    else:
        form = PostForm()

    return render(request, "create_post.html", {"form": form})

<<<<<<< HEAD
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('board')

def download_audio(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    response = HttpResponse(post.audio_file.read(), content_type='audio/mpeg')
    response['Content-Disposition'] = f'attachment; filename="{post.audio_file.name}"'
    return response
=======

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the current user has permission to delete the post
    if request.user == post.author or request.user.is_superuser:
        post.delete()

    return redirect("board")
>>>>>>> eeb6e9f7fb30e90dea0759d077c4b75b2f9bc960
