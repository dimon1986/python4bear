from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from .models import Topic, Post, Comment
from .forms import PostForm, CommentForm, EmailPostForm
from taggit.models import Tag
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from images.models import Image
from django.http import HttpResponse
from actions.utils import create_action


def similar():
    #
    # List of similar posts
    similar_posts = Post.published.filter()
    similar_posts = similar_posts.order_by('views')[:3]
    return similar_posts

def image_foor(request):
    image_js = Image.objects.all().order_by('-created')
    paginator = Paginator(image_js, 4)
    page = request.GET.get('page')
    try:
        image_js = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом
        image_js = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если запрос AJAX и страница вне диапазона
            # вернуть пустую страницу
            return HttpResponse('')
    return image_js

def hell(request):
    #Возврат html докуменда домашний страницы всех Тем.
    queryset_post = Post.objects.filter(status='published').order_by('-publish')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset_post, 3)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставьте первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # вероятно, пользователь попытался добавить номер страницы
        # в url, поэтому мы переходим к последней странице
        posts = paginator.page(paginator.num_pages)


    similar_posts = similar()
    image_js=image_foor(request)

    context = {'posts': posts, 'queryset_post':queryset_post, 'similar_posts': similar_posts, 'image_js':image_js}
    return render(request, 'python4bear/hell.html', context)


def home(request):
    #Возврат html докуменда домашний страницы всех Тем.
    queryset = Topic.objects.order_by('date_added')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 5)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставьте первую страницу
        topics = paginator.page(1)
    except EmptyPage:
        # вероятно, пользователь попытался добавить номер страницы
        # в url, поэтому мы переходим к последней странице
        topics = paginator.page(paginator.num_pages)

    similar_posts = similar()
    image_js = image_foor(request)

    context = {'topics': topics, 'similar_posts': similar_posts, 'image_js':image_js,}
    return render(request, 'python4bear/home.html', context)


def posts_all(request, pk, tag_slug=None):
    """Возврат html докуменда одной Темы и всё её Посты."""
    # можно и так если без того класса Post.objects.filter(status='published')
    topic = get_object_or_404(Topic, pk=pk)
    queryset = topic.posts.order_by('-views').annotate(replies=Count('comment'))

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags__in=[tag])

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        posts = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        posts = paginator.page(paginator.num_pages)

        # List of similar posts
    similar_posts = Post.published.filter(topic__pk=pk)
    similar_posts = similar_posts[:3]
    image_js = image_foor(request)

    context = {'topic':topic, 'posts':posts,
               'page': page, 'tag': tag,
               'similar_posts': similar_posts,
               'image_js': image_js,
               'sent': request.GET.get('sent', False)}

    return render(request, 'python4bear/posts_all.html', context)


def view_post(request, pk, post_name):
    """Просматриваем конкретный Пост"""
    post = get_object_or_404(Post, topic__pk=pk,
                             slug=post_name,)
    comments = post.comment.filter(active=True)

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

            # думал так можно заставить не считать обрати внимание как ретурн делается
            """  переносим код в модели!!!  return HttpResponseRedirect(
                '{}?sent=True'.format(reverse('python4bear:view_post',
                                              kwargs={'pk':post.topic.pk, 'post_name':post.slug})))"""
            return HttpResponseRedirect(
                '{}?sent=True'.format(post.get_absolute_url()))

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    image_js = image_foor(request)

    context = {'post':post, 'form': form,
               'comments':comments, 'similar_posts': similar_posts,
               'image_js': image_js,
               'sent': request.GET.get('sent', False)}

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
            create_action(request.user, 'создал пост', new_post)
            return HttpResponseRedirect(
                '{}?sent=True'.format(reverse('python4bear:posts_all',
                                          kwargs={'pk': topic.pk})))

    context = {'topic': topic, 'form': form}
    return render(request, 'python4bear/new_post.html', context)


@login_required
def edit_post(request, pk, post_name):
    post = get_object_or_404(Post, slug=post_name,)
    topic = post.topic
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('python4bear:view_post', pk=pk, post_name=post.slug,)

    context = { 'topic': topic, 'post': post, 'form': form}
    return render(request, 'python4bear/edit_post.html', context)


@login_required
def post_share(request, post_name):
    # Retrieve post by id
    post = get_object_or_404(Post, slug=post_name, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = 'Почитай отца и мать и возможно пост про {}'.format(post.title)
            message = 'Тема "{}" адрес {}\n\'коментарий: {}'.format(post.title, post_url, cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'python4bear/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


