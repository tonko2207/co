from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm


# --- PUBLICZNE (dla wszystkich) ---

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    return render(request, "marketing/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status="published")
    return render(request, "marketing/post_detail.html", {"post": post})


# --- PANEL MARKETINGU (CRUD) ---

@login_required
@permission_required("marketing.view_post", raise_exception=True)
def manage_posts(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "marketing/manage_posts.html", {"posts": posts})


@login_required
@permission_required("marketing.add_post", raise_exception=True)
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("marketing:post_list")
    else:
        form = PostForm()

    return render(request, "marketing/post_form.html", {"form": form})

@login_required
@permission_required("marketing.change_post", raise_exception=True)
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("marketing:manage_posts")

    return render(request, "marketing/post_form.html", {"form": form})


@login_required
@permission_required("marketing.delete_post", raise_exception=True)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect("marketing:manage_posts")

    return render(request, "marketing/post_confirm_delete.html", {"post": post})