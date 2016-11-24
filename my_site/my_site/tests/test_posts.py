import unittest
from unittest.mock import MagicMock

from my_site.my_site.posts import Post
from my_site.my_site.posts import PostList


class PostListTests(unittest.TestCase):
    def setUp(self):
        self.application = MagicMock()
        self.flatpages = MagicMock()

    def test_total_post_count(self):
        my_posts = PostList(self.application, self.flatpages)
        my_posts.append(Post())
        my_posts.append(Post())
        my_posts.append(Post())
        my_posts.append(Post())
        my_posts.append(Post())
        self.assertEqual(5, my_posts.total_post_count)

    def test_has_previous_page(self):
        raise NotImplementedError

    def test_has_next_page(self):
        raise NotImplementedError
