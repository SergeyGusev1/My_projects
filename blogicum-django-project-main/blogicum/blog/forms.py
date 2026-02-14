from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'text', 'pub_date',
            'author', 'category', 'location',
            'image', 'is_published'
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
