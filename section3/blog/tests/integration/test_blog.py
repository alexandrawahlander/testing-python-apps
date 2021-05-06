from unittest import TestCase
from blog import Blog

class BlogTest(TestCase):
    def test_create_post_in_blog(self):
        b = Blog("Testbloggen", "Alexandra Wåhlander")
        b.create_post("Test post", "Test Content")

        self.assertEqual(len(b.posts), 1)
        self.assertEqual(b.posts[0].title, "Test post")
        self.assertEqual(b.posts[0].content, "Test Content")

    def test_json(self):
        b = Blog("Testbloggen", "Alexandra Wåhlander")
        b.create_post("Test post", "Test Content")

        expected = {"Title": "Testbloggen",
                    "Author": "Alexandra Wåhlander",
                    "Posts": [
                        {"title": "Test post",
                               "content": "Test Content"}]
                    }
        self.assertDictEqual(expected, b.json())

    def test_json_no_posts(self):
        b = Blog("Testbloggen", "Alexandra Wåhlander")
        expected = {"Title": "Testbloggen",
                    "Author": "Alexandra Wåhlander",
                    "Posts": []
                    }

        self.assertDictEqual(expected, b.json())