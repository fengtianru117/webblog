from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets={
            'content':forms.Textarea(attrs={'style': 'vertical-align:top'})
        }