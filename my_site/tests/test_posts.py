import unittest
from my_site.posts import PostList
from my_site.posts import Post


class PostListTests(unittest.TestCase):
    def test_total_post_count(self):
        my_posts = PostList()
        my_posts.append(Post())
        my_posts.append(Post())
        my_posts.append(Post())
        my_posts.append(Post())
        my_posts.append(Post())
        self.assertEqual(5, my_posts.total_post_count)
