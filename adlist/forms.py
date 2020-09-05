from .models import Comment
from django import forms
from django.forms import Textarea
from .models import Ad


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['text'].widget = Textarea(attrs={'rows': 5})
