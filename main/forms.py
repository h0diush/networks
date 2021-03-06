from django import forms

from main.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'group', 'image', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
