import unittest
from unittest.mock import MagicMock

import my_site.my_site.routes


class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.application = MagicMock()
        self.flatpages = MagicMock()

    def test_route_basic_blog(self):
        rendered_html = my_site.my_site.routes.blog()
        with open('test_data/basic_blog_html.txt') as expected_result_hdl:
            self.assertEqual(rendered_html, expected_result_hdl.read())

    def test_route_basic_single_blog_post(self):
        rendered_html = my_site.my_site.routes.single_blog_post('unit_test_post_one')
        with open('test_data/basic_single_blog_post_html.txt') as expected_result_hdl:
            self.assertEqual(rendered_html, expected_result_hdl.read())

    def test_route_about(self):
        rendered_html = my_site.my_site.routes.about()
        with open('test_data/about_html.txt') as expected_result_hdl:
            self.assertEqual(rendered_html, expected_result_hdl.read())
