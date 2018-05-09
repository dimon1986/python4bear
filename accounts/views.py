from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate

from accounts.forms import UserForm, ProfileEditForm, UserFormForEdit
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact

from actions.utils import create_action
from actions.models import Action

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, \
PageNotAnInteger

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
            new_user.email = form.cleaned_data['email']
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            create_action(new_user, 'создал учетную запись тут:)')
            profile.save()# вот это походу не надо он и так создается!или!
            # Выполнение входа и перенаправление на домашнюю страницу
            authenticated_user = authenticate(username=form.cleaned_data['username'],
                                              password=form.cleaned_data['password'])
            login(request, authenticated_user)
            return redirect('python4bear:home')
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@login_required
def edit_account(request):
    """Пользовательский аккаунт, его редактирование"""

    user_form = UserFormForEdit(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль - обновился!')
        else:
            messages.error(request, 'Error ты, что-то накасячел.')

        return HttpResponseRedirect('{}?sent=True'.format(reverse('accounts:my_account')))

    return render(request, 'accounts/my_account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# @login_required
# def user_list(request):
#     # лист пользователь можно сделать пагинацию!!
#     users = User.objects.filter(is_active=True)
#     return render(request, 'accounts/user/list.html', {'section': 'people',
#                                                       'users': users})


def user_list(request):
    users = User.objects.filter(is_active=True).order_by('id')# если ордер бай ай ди не добавляю возникает ошибка
    paginator = Paginator(users, 4)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом
        users = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если запрос AJAX и страница вне диапазона
            # вернуть пустую страницу
            return HttpResponse('')
        # Если страница находится вне диапазона доставить последнюю страницу результатов
        users = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'accounts/user/list_ajax.html',
                      {'section': 'people', 'users': users})
    return render(request,
                  'accounts/user/list.html',
                  {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    view_user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'accounts/user/detail.html', {'section': 'people',
                                                        'view_user': view_user})

@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user1 = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user1)
                create_action(request.user, ' подписался на ', user1)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user1).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})

# def track(request):
#     # Показать все действия по умолчанию
#     actions = Action.objects.exclude(user=request.user)
#     following_ids = request.user.following.values_list('id',
#                                                        flat=True)
#     if following_ids:
#         # Если пользователь следит за другими, извлекайте только их действия
#         actions = actions.filter(user_id__in=following_ids) \
#             .select_related('user', 'user__profile') \
#             .prefetch_related('target')
#     actions = actions[:10]
#
#     context = {'actions': actions, }
#
#     return render(request, 'accounts/user/track.html', context)


@login_required
def track(request):
    # Показать все действия по умолчанию
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # Если пользователь следит за другими, извлекайте только их действия
        actions = actions.filter(user_id__in=following_ids) \
            .select_related('user', 'user__profile') \
            .prefetch_related('target')
        paginator = Paginator(actions, 10)
        page = request.GET.get('page')
        try:
            actions = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом
            actions = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                # Если запрос AJAX и страница вне диапазона
                # вернуть пустую страницу
                return HttpResponse('')
            # Если страница находится вне диапазона доставить последнюю страницу результатов
            actions = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request,
                          'accounts/user/track_ajax.html',
                          {'section': 'actions', 'actions': actions})
        return render(request,
                      'accounts/user/track.html',
                      {'section': 'actions', 'actions': actions})
