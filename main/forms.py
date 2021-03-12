from django import forms

from main.models import Comment, Post, Rating


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'group', 'image',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', ]
        widgets = {
         'rating': forms.TextInput(attrs={'type': 'range', 'class': "form-range", 'min': "1", 'max': "10", 'step': "1", 'id': "customRange3"})
         }

