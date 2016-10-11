from datetime import datetime
from mock import Mock, patch
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.blog import consumer
from us_ignite.blog.models import Post, PostAttachment


class TestParseDateFunction(TestCase):

    def test_date_is_parsed_correctly(self):
        date_string = '2014-01-13 16:05:47'
        date = consumer.parse_date(date_string)
        ok_(isinstance(date, datetime))
        eq_(date.tzinfo.zone, 'America/New_York')
        eq_(date.year, 2014)
        eq_(date.month, 1)
        eq_(date.day, 13)
        eq_(date.hour, 16)
        eq_(date.minute, 5)


def _get_post_data(**kwargs):
    data = {
        'id': 23,
        'type': 'post',
        'title': 'Gigabit Post',
        'slug': 'gigabit-post',
        'content': 'Content',
        'excerpt': 'Excerpt',
        'author': {},
        'date': '2014-01-13 16:05:47',
        'modified': '2014-01-13 16:05:47',
        'url': 'http://us-ignite.org/',
        'categories': [],
        'tags': [],
    }
    data.update(kwargs)
    return data


class TestImportPostFunction(TestCase):

    @patch.object(Post, 'save')
    @patch('us_ignite.blog.consumer.get_author')
    def test_post_is_imported_correctly(self, mock_get, mock_save):
        user = User(username='foo', id=2)
        mock_get.return_value = user
        data = _get_post_data()
        post = consumer.import_post(data)
        mock_save.assert_called_once_with()
        eq_(post.wp_id, 23)
        eq_(post.wp_url, 'http://us-ignite.org/')
        eq_(post.author, user)
        eq_(post.wp_type, 'post')
        eq_(post.title, 'Gigabit Post')
        eq_(post.content, 'Content')
        eq_(post.content_html, 'Content')
        eq_(post.excerpt, 'Excerpt')
        eq_(post.excerpt_html, 'Excerpt')
        ok_(post.publication_date)
        ok_(post.update_date)

    @patch('us_ignite.blog.consumer.get_author')
    @patch('us_ignite.blog.models.Post.objects.get')
    def test_existing_custom_post_is_ignored(self, mock_get, mock_author):
        post_double = Post(id=12, is_custom=True)
        mock_get.return_value = post_double
        data = _get_post_data(id=10)
        post = consumer.import_post(data)
        mock_get.assert_called_once_with(wp_id__exact=10)
        eq_(post, post_double)
        eq_(mock_author.call_count, 0)


class TestConsumeFunction(TestCase):

    @patch('us_ignite.blog.consumer.import_post')
    @patch('requests.get')
    def test_consumer_is_executed_successfully(self, mock_get, mock_import):
        response_mock = Mock()
        response_mock.json.return_value = {}
        mock_get.return_value = response_mock
        post_list = consumer.consume()
        mock_get.assert_called_once_with(
            'http://us-ignite.org/',
            params={'count': 1000, 'json': 'get_recent_posts'})
        response_mock.json.assert_called_once_with()
        eq_(mock_import.call_count, 0)
        eq_(post_list, [])


def _get_attachment_data(**kwargs):
    data = {
        'id': 3367,
        'title': 'Image',
        'slug': 'image',
        'url': 'http://us-ignite.org/image.jpg',
        'mime_type': 'image/jpeg',
        'description': '',
        'caption': '',
    }
    data.update(kwargs)
    return data


class TestImportAttachmentFunction(TestCase):

    @patch('us_ignite.common.files.import_file')
    @patch.object(PostAttachment, 'save')
    def test_attachment_is_created_successfully(self, mock_save, mock_file):
        data = _get_attachment_data()
        mock_post = Post()
        attachment = consumer.import_attachment(mock_post, data)
        eq_(attachment.wp_id, '3367')
        eq_(attachment.title, 'Image')
        eq_(attachment.slug, 'image')
        eq_(attachment.url, 'http://us-ignite.org/image.jpg')
        eq_(attachment.mime_type, 'image/jpeg')
        eq_(attachment.description, '')
        eq_(attachment.caption, '')
        eq_(attachment.post, mock_post)
        mock_save.assert_called_once_with()
        mock_file.assert_called_once_with(
            'http://us-ignite.org/image.jpg', 'blog/image.jpg')


class TestGetTagListFunction(TestCase):

    def test_get_tag_list_is_successful(self):
        data = [
            {'title': 'Events', 'post_count': 22, 'slug': 'events', 'id': 4},
            {'title': 'News', 'post_count': 35, 'slug': 'news', 'id': 6},
        ]
        tag_list = consumer.get_tag_list(data)
        eq_(sorted(tag_list), ['Events', 'News'])


class TestKeyFromURLHelper(TestCase):

    def test_key_is_generated_successfully(self):
        key = consumer._get_key_from_url(
            'http://us-ignite.org/image.jpg', prefix='foo')
        eq_(key, 'foo/image.jpg')
