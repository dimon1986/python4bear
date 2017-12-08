from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate

from accounts.forms import UserForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

# Create your views here.
def logout_view(request):
    """Завершает сеанс работы с приложением."""
    logout(request)
    return HttpResponseRedirect(reverse('python4bear:home'))


def signup(request):
    """Регистрирует нового пользователя."""
    if request.method != 'POST':
        # Показать пустую регестрационную форму
        form = UserForm()
    else:
        # Обработка заполненной формы.
        form = UserForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Выполнение входа и перенаправление на домашнюю страницу
            authenticated_user = authenticate(username=form.cleaned_data['username'],
                                              password=form.cleaned_data['password'])
            login(request, authenticated_user)
            return redirect('python4bear:home')
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('accounts:my_account')

    def get_object(self):
        return self.request.user