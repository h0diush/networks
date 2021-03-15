from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg
from django.contrib import messages
from django.core.paginator import Paginator

from main.forms import CommentForm, PostForm, RatingForm
from main.models import Comment, Follow, Group, Like, Post, Rating, User


def index(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(title__icontains=search_query)
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
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
    rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))
    rating_us = post.rating.all()
    rating_all = []
    rating_bool = False
    for rt in rating_us:
        rating_user = rt.user
        rating_all.append(rating_user)
    if request.user in rating_all:
        rating_bool = True
    form = CommentForm()
    form_rating = RatingForm()
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
        'like': like,
        'form_rating': form_rating,
        'rating': rating,
        'rating_bool': rating_bool}
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
        messages.success(request, 'Вы поставили оценку')
        return redirect('detail', pk)
    context = {'form': form, 'post': post}
    return render(request, 'comments.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    followers = []
    follow = False
    following = user.following.all()
    for us in following:
        author_foll = us.user
        followers.append(author_foll)
    if request.user in followers:
        follow = True
    context = {'user': user, 'posts': posts, 'follow': follow}
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


@login_required
def profile_follow(request, username):
    author_post = get_object_or_404(User, username=username)
    if request.user != author_post:
        Follow.objects.create(user=request.user, author=author_post)
    return redirect('profile', username)


def profile_unfollow(request, username):
    author_post = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=request.user)
    follow = Follow.objects.filter(author=author_post, user=user)
    follow.delete()
    return redirect('profile', username)


@login_required
def myprofile(request, username):
    user = get_object_or_404(User, username=username)
    post = user.posts.all()
    post_list = Post.objects.filter(author__following__user=request.user)
    context = {'posts': post, 'posts_list': post_list}
    return render(request, 'myprofile.html', context)


@login_required
def delete_comment(request, pk, comment_id):   
    post = Post.objects.get(id=pk) 
    comment = Comment.objects.get(id=comment_id)
    if comment.author == request.user:
        comment.delete()    
    return redirect('detail', pk)


@login_required
def add_rating(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = RatingForm(request.POST or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.post = post
        new_form.user = request.user
        new_form.save()
        return redirect('detail', pk)
    context = {'form': form, 'post': post}
    return render(request, 'add_rating.html', context)

    

