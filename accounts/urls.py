from django.conf.urls import url
from django.contrib.auth.views import login, PasswordChangeView, PasswordChangeDoneView
from . import views

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,  PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    # Страница выхода.
    url(r'^logout/$', views.logout_view, name='logout'),
    #регистрация вроди как, уже мозг кипит....
    url(r'^signup/$', views.signup, name='signup'),
    # ссылка на изменение имяни, фамилии и почты
    url(r'^settings/account/$', views.UserUpdateView.as_view(), name='my_account'),

    # Если забыли пароль вот это всё решит ваши проблемы |
    url(r'^reset/$', PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'),
        name='password_reset'),

    url(r'^reset/done/$', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),

    url(r'^reset/complete/$', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

    # если сами решили сменить в своём профиле
    url(r'^settings/password/$', PasswordChangeView.as_view(template_name='accounts/password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),


]