from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment
from django import forms
from django.forms import Textarea


class UserCreate(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['text'].widget = Textarea(attrs={'rows': 5})
