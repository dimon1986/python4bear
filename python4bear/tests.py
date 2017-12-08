from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
from django.core.urlresolvers import reverse
from django.urls import resolve
from .views import home, posts, new_post, posts_comments
from .models import Topic, Post, Comment
from .forms import PostForm, CommentForm

class HomeTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(text='Django', description='Django board.')
        url = reverse('python4born:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        posts_url = reverse('python4bear:posts', kwargs={'pk': self.topic.pk})
        self.assertContains(self.response, 'href="{0}"'.format(posts_url))

class TopicsPostsTests(TestCase):
    def setUp(self):
        Topic.objects.create(text='Django', description='Django board.')

    def test_topics_posts_view_success_status_code(self):
        url = reverse('python4bear:posts', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_topics_posts_view_contains_link_back_to_homepage(self):
        entrys_url = reverse('python4bear:posts', kwargs={'pk': 1})
        response = self.client.get(entrys_url)
        homepage_url = reverse('python4bear:home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_topics_posts_view_not_found_status_code(self):
        url = reverse('python4bear:posts', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_topics_posts_url_resolves_topics_posts_view(self):
        view = resolve('/posts/1/')
        self.assertEquals(view.func, posts)

    def test_topics_posts_view_contains_navigation_links(self):
        topics_posts_url = reverse('python4bear:posts', kwargs={'pk': 1})
        homepage_url = reverse('python4bear:home')
        new_post_url = reverse('python4bear:new_post', kwargs={'pk': 1})

        response = self.client.get(topics_posts_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_post_url))

class NewPostTests(TestCase):
    def setUp(self):
        Topic.objects.create(text='Django', description='Django board.')
        User.objects.create_user(username='dima', email='dima@bk.com', password='32167')  # <- included this line here

    def test_new_post_view_success_status_code(self):
        url = reverse('python4bear:new_post', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_post_view_not_found_status_code(self):
        url = reverse('python4bear:new_post', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_post_url_resolves_new_post_view(self):
        view = resolve('/post/1/new/')
        self.assertEquals(view.func, new_post)

    def test_new_post_view_contains_link_back_to_topic_posts_view(self):
        new_post_url = reverse('python4bear:new_post', kwargs={'pk': 1})
        topics_url = reverse('python4bear:posts', kwargs={'pk': 1})
        response = self.client.get(new_post_url)
        self.assertContains(response, 'href="{0}"'.format(topics_url))

    def test_csrf(self):
        url = reverse('python4bear:new_post', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_post_valid_comment_data(self):
        url = reverse('python4bear:new_post', kwargs={'pk': 1})
        data = {
            'title': 'Test title',
            'text': 'Lorem ipsum dolor sit amet',
        }
        response = self.client.post(url, data)
        self.assertTrue(Post.objects.exists())

    def test_new_post_invalid_comment_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('python4bear:new_post', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('python4bear:new_post', kwargs={'pk': 1})
        data = {
            'title': '',
            'text': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Post.objects.exists())
        self.assertFalse(Comment.objects.exists()) # я нифига не понимаю... вот это

    def test_contains_form(self):  # <- new test
        url = reverse('python4bear:new_post', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('python4bear:new_post', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


class LoginRequiredNewPostTests(TestCase):
    def setUp(self):
        Post.objects.create(title='Test title', text='text',)
        self.url = reverse('python4bear:new_post', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('accounts:login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class TopicCommentsTests(TestCase):
    def setUp(self):
        topic = Topic.objects.create(text='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        post = Post.objects.create(title='Test title', text='text', topic=topic, owner=user)
        Comment.objects.create(text='Lorem ipsum dolor sit amet', post=post, owner=user)
        url = reverse('python4born:posts_comments', kwargs={'pk': topic.pk, 'post_pk': post.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/topic/1/posts/1/')
        self.assertEquals(view.func, posts_comments)