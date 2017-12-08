from django import forms

from .models import Topic, Post, Comment

class PostForm(forms.ModelForm):
    text = forms.CharField(label='Содержание',
        widget=forms.Textarea(attrs={'rows': 5,
                                     'placeholder':
                                         'Тут можно писать огромный пост, но подумай, оно тебе надо?'}),
    )
    class Meta:
        model = Post
        fields = ['title','text', 'image']


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Текст',
        widget=forms.Textarea(attrs={'rows': 5,
                                     'placeholder': 'Ну давай странник, срази всех остроумием.'}),
        max_length=3000,
        help_text='Максимальная длина комента 3000 символов, так что думай, прежде чем писать.',
    )
    class Meta:
        model = Comment
        fields = ['text']
