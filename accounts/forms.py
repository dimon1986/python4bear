from django import forms

from django.contrib.auth.models import User

"""Тут кривые тесты, я не понимаю, надо то обдумывать и с этим решать"""

class UserForm(forms.ModelForm):
    """Форма для юзера измененная"""
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2' ]

    def clean_password2(self):
        word = self.cleaned_data
        if word['password'] != word['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return word['password']