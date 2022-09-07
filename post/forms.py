from turtle import width
from django.forms import ModelForm
from django import forms
from post.models import Post, SubPost, Comment
from ckeditor.fields import RichTextField


class SubPostModelForm(ModelForm):
    class Meta:
        model = SubPost
        fields = ['title', 'description', 'resources']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title for the SubPost',  'class': 'form-control', }),
            'description': forms.Textarea(attrs={'class': 'form-control', }),
            'resources': forms.TextInput(attrs={'placeholder': 'Add only resource links',  'class': 'form-control', }),
        }


class PostCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'category',
            'image',
            'content',
        )
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title for the Post', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
