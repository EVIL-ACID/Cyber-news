from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from cybernews.models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields  = ['post_title', 'post_link', 'post_text']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)