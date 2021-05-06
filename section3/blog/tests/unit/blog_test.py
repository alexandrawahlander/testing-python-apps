from unittest import TestCase
from blog import Blog

class BlogTest(TestCase):
    def test_create_blog(self):
        b = Blog("Testbloggen", "Alexandra Wåhlander")

        self.assertEqual("Testbloggen", b.title)
        self.assertEqual("Alexandra Wåhlander", b.author)
        self.assertEqual([], b.posts)

    def test_repr(self):
        b = Blog("Testbloggen", "Alexandra Wåhlander")

        self.assertEqual("Testbloggen by Alexandra Wåhlander (0 posts)", b.__repr__())

    def test_repr_multiple_posts(self):
        b = Blog("Testbloggen", "Alexandra Wåhlander")
        b.posts = ["test", "Hej"]

        b2 = Blog("Testbloggen", "Alexandra Wåhlander")
        b2.posts = []

        b3 = Blog("Testbloggen", "Alexandra Wåhlander")
        b3.posts = ["Ett"]

        self.assertEqual("Testbloggen by Alexandra Wåhlander (2 posts)", b.__repr__())
        self.assertEqual("Testbloggen by Alexandra Wåhlander (0 posts)", b2.__repr__())
        self.assertEqual("Testbloggen by Alexandra Wåhlander (1 post)", b3.__repr__())


   # def test_json(self):
    #    b = Blog("Testbloggen", "Alexandra Wåhlander")
     #   expected = {"Title": Testbloggen, "Author": Alexandra Wåhlander, "Posts": []}

      #  self.assertEqual(expected, b.json())