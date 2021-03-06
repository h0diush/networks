from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import CommentForm, PostForm
from main.models import Group, Like, Post, User


def index(request):
    posts = Post.objects.all()
    # paginator
    context = {'posts': posts}
    return render(request, 'index.html', context)


def group(request):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'group.html', context)


def group_id(request, slug):
    groups = get_object_or_404(Group, slug=slug)
    posts = groups.posts.all()
    context = {'posts': posts}
    return render(request, 'group_detail.html', context)


def post_id(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.all()
    count = post.comments.count()
    form = CommentForm()
    likes = post.likes.all()
    like = False
    post_likes = []
    for us in likes:
        user_like = us.user
        post_likes.append(user_like)
    if request.user in post_likes:
        like = True
    context = {
        'comments': comments,
        'post': post,
        'form': form,
        'count': count,
        'like': like}
    return render(request, 'post_id.html', context)


@login_required
def new_post(request):
    form = PostForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.author = request.user
        new_form.save()
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    if post.author != request.user:
        redirect('detail', pk)
    form = PostForm(request.POST, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('detail', pk)
    return render(request, 'post_edit.html', {'form': form, 'post': post})


@login_required
def delete(request, pk):
    post = Post.objects.get(id=pk)
    if post.author != request.user:
        return redirect('detail', pk)
    post.delete()
    return render(request, 'delete.html')


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('detail', pk)
    context = {'form': form, 'post': post}
    return render(request, 'comments.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    context = {'user': user, 'posts': posts}
    return render(request, 'profile.html', context)


@login_required
def like(request, pk):
    post = Post.objects.get(id=pk)
    Like.objects.get_or_create(user=request.user, post=post)
    return redirect('detail', pk)


@login_required
def not_like(request, pk):
    post = Post.objects.get(id=pk)
    post_like = Like.objects.get(user=request.user, post=post)
    post_like.delete()
    return redirect('detail', pk)
