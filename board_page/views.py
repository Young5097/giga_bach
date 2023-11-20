from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required


# Create your views here.
def board(request):
    posts = Post.objects.all()
    return render(request, "board.html", {"posts": posts})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("board")  # 게시글 목록 페이지로 이동
    else:
        form = PostForm()

    return render(request, "create_post.html", {"form": form})
