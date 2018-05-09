from django.conf.urls import url
from . import views
from django.urls import reverse_lazy

from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

urlpatterns = [
    # Страница входа.
    url(r'^login/$', LoginView.as_view
    (template_name='accounts/registration/login.html'), name='login'),
    # Страница выхода.
    url(r'^logout/$', views.logout_view, name='logout'),
    #регистрация вроде, как...
    url(r'^signup/$', views.signup, name='signup'),
    # ссылка на изменение имяни, фамилии и почты вобщем настройки аккаунта
    url(r'^accounts/profile/$', views.edit_account, name='my_account'),


    # смена пароля под своим аккаунтом
    url(r'^password-change/$', PasswordChangeView.as_view(
        template_name='accounts/registration/password_change.html',
        success_url=reverse_lazy('accounts:password_change_done')
    ),
        name='password_change'),

    url(r'^password-change-done/$', PasswordChangeDoneView.as_view(
        template_name='accounts/registration/password_change_done.html'),
        # если что лизи
        name='password_change_done'),

    # Если забыли пароль вот это всё решит ваши проблемы |
    url(r'^password-reset/$', PasswordResetView.as_view(
        template_name='accounts/registration/password_reset.html',
        email_template_name='accounts/registration/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
    ),
        name='password_reset'),

    url(r'^password-reset/done/$', PasswordResetDoneView.as_view(
        template_name='accounts/registration/password_reset_done.html',),
        name='password_reset_done'),

    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        PasswordResetConfirmView.as_view(
            template_name='accounts/registration/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete'),
        ),
        name='password_reset_confirm'),

    url(r'^password-reset/complete/$',
        PasswordResetCompleteView.as_view(
            template_name='accounts/registration/password_reset_complete.html',
        ),
        name='password_reset_complete'),


    # только так сначало фолловерз, а потом все для него иначе джскрипт не сработает
    url(r'^users/followers/$', views.user_follow, name='user_follow'),

    # лист пользователей
    url(r'^users/$', views.user_list, name='user_list'),

    # конкретный юзер
    url(r'^users/(?P<username>[-\w]+)/$',
        views.user_detail, name='user_detail'),
    # новости по сути
    url(r'^track/$', views.track, name='track'),




]
