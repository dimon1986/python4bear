from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView, CreateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

from .models import Topic, Post, Comment
from .forms import PostForm, CommentForm



class TopicListView(ListView):
    """Возврат html докуменда домашний страницы всех Тем."""
    model = Topic
    context_object_name = 'topics'
    template_name = 'python4bear/home.html'
    paginate_by = 5


class PostsAllListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'python4bear/posts_all.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk=self.kwargs.get('pk'))
        queryset = self.topic.posts.order_by('-date_added').annotate(replies=Count('comment'))
        return queryset


def view_post(request, pk, post_pk):
    """Просматриваем конкретный Пост"""
    post = get_object_or_404(Post, topic__pk=pk, pk=post_pk)

    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = CommentForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = CommentForm(request.POST, )
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.owner = request.user
            new_comment.save()
            post.views += 1
            post.save()
            post.date_added = timezone.now()  # обнавляю дату поста


        return redirect('python4bear:view_post', pk=post.topic.pk, post_pk=post.pk)

    context = {'post':post, 'form': form}
    return render(request, 'python4bear/view_post.html', context)


@login_required
def new_post(request, pk):
    """Добавляет новый Пост к конкретной Теме."""
    topic = get_object_or_404(Topic, pk=pk)
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = PostForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.topic = topic
            new_post.owner = request.user
            new_post.save()
            return redirect('python4bear:posts_all', pk=topic.pk)

    context = {'topic': topic, 'form': form}
    return render(request, 'python4bear/new_post.html', context)

"""class NewPostView(CreateView):
    #Я ТАК И НЕ ПРИДУМАЛ КАК ЗАСТАВИТЬ ЕГО РАБОТАТЬ, ТАК КАК НЕ ПОНИМАЮ
    #КАК ПЕРЕДАВАТЬ ПРEМАРИ КЕЙ В ШАБЛОН
    form_class = PostForm
    template_name = 'python4bear/new_post.html'
    pk_url_kwarg = 'topic_pk'
    context_object_name = 'topic'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner = self.request.user
        post.date_added = timezone.now()
        post.save()
        return redirect('python4bear:posts_all, topic_pk=topic.pk')"""


"""@login_required
def edit_post(request, pk, post_pk):

    post = get_object_or_404(Post, topic__pk=pk, pk=post_pk)
    topic = post.topic
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('python4bear:view_post', pk=pk, post_pk=post_pk)

    context = { 'topic': topic, 'post': post, 'form': form}
    return render(request, 'python4bear/edit_post.html', context)"""

@method_decorator(login_required, name='dispatch')
class PostEditView(UpdateView):
    """ # Редактирование поста владельцем!
    работает, но не работает защита от Чужего!! Заработало!! сменил декоратор:))"""
    model = Post
    fields = ('title', 'text', 'image')
    template_name = 'python4bear/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner = self.request.user
        post.date_added = timezone.now()
        post.save()
        return redirect('python4bear:view_post', pk=post.topic.pk, post_pk=post.pk)



