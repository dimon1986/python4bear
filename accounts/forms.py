from django import forms

from django.contrib.auth.models import User

from .models import Profile

class UserForm(forms.ModelForm):
    """Форма юзера..."""
    email = forms.EmailField( max_length=50, required=True, )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean_password2(self):
        word = self.cleaned_data
        if word['password'] != word['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return word['password']

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(("Пользователь с таким email уже существует!"))

class UserFormForEdit(forms.ModelForm):
    """Форма для редактирования юзера, не все поля доступны специально"""
    email = forms.EmailField(max_length=50, required=True, )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo',]