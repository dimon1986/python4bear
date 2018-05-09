from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    text = forms.CharField(label='Содержание', widget=CKEditorUploadingWidget(config_name='awesome',
                                                 attrs={ 'rows': 5, 'placeholder':
                                                   'Тут можно писать огромный пост, но подумай, оно тебе надо?'},
        )
    )
    class Meta:
        model = Post
        fields = ['title','text', ]



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

class EmailPostForm(forms.Form):
    to = forms.EmailField(label='Кому отправить?',)
    comments = forms.CharField(label='Коментарий',
                               required=False,
                               widget=forms.Textarea(attrs={
                                   'placeholder': 'Что бы не забыть зачем отправил.'}))

