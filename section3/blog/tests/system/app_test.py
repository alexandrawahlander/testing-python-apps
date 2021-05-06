from unittest import TestCase
from unittest.mock import patch, call

import app
from blog import Blog
from post import Post


class AppTest(TestCase):
    def setUp(self):
        blog = Blog('Test', 'Test author')
        app.blogs = {'Test': blog}

    def test_menu_prints_prompt(self):
        with patch("builtins.input", return_value='q') as mocked_input:
            app.menu()
            mocked_input.assert_called_with(app.MENU_PROMPT)
            print("test_menu_prints_prompt: " + mocked_input.return_value)

    def test_menu_calls_print_blogs(self):
        with patch("app.print_blogs") as mocked_print_blogs:
            with patch("builtins.input", return_value='q'):
                app.menu()
                mocked_print_blogs.assert_called()

    def test_menu_calls_create_blog(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('c', 'Test Create Blog', 'Test Author', 'q')

            app.menu()

            self.assertIsNotNone(app.blogs['Test Create Blog'])

    def test_menu_calls_create_blog2(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.ask_create_blog') as mocked_ask_create_blog:
                mocked_input.side_effect = ('c', 'Test Create Blog', 'Test Author', 'q')

                app.menu()

                mocked_ask_create_blog.assert_called()

    def test_menu_calls_ask_read_blog(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.ask_read_blog') as mocked_ask_read_blog:
                mocked_input.side_effect = ('r', 'Test blog title', 'q')

                app.menu()

                mocked_ask_read_blog.assert_called()




    def test_menu_calls_ask_create_post(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.ask_create_post') as mocked_ask_create_post:
                mocked_input.side_effect = ('p', 'Test', 'New Post', 'New Content', 'q')
                app.menu()

                mocked_ask_create_post.assert_called()



    def test_print_blogs(self):
     #   blog = Blog("Test", "Test author")
      #  app.blogs = {"Test": blog}

        with patch("builtins.print") as mocked_print:
            app.print_blogs()
            mocked_print.assert_called_with("- Test by Test author (0 posts)")

    def test_print_blogs_empty(self):
        app.blogs = {}

        with patch("builtins.print") as mocked_print:
            app.print_blogs()
            mocked_print.assert_called_with("No blogs")

    def test_print_blogs_many(self):
        blog1 = Blog("Title1", "Author1")
        blog2 = Blog("Title2", "Author2")
        app.blogs = {"Title1": blog1, "Title2": blog2}

        with patch("builtins.print") as mocked_print:
            app.print_blogs()
            assert mocked_print.call_args_list[0] == call("- Title1 by Author1 (0 posts)")
            assert mocked_print.call_args_list[1] == call("- Title2 by Author2 (0 posts)")



    def test_ask_create_blog(self):
        with patch('builtins.input', return_value='Test') as mocked_input:
            print("test_ask_create_blog: " + mocked_input.return_value)
            mocked_input.side_effect = ('Test', 'Test Author')
            app.ask_create_blog()

            self.assertIsNotNone(app.blogs.get('Test'))

    def test_ask_read_blog(self):
        blog = Blog("Test", "Test author")
        app.blogs = {"Test": blog}

        with patch('builtins.input', return_value='Test'):
            with patch('app.print_posts') as mocked_print_posts:
                app.ask_read_blog()

                mocked_print_posts.assert_called_with(blog)

    def test_print_posts(self):
        blog = Blog("Test", "Test author")
        blog.create_post("Test Post", "Test content")
        app.blogs = {"Test": blog}

        with patch('app.print_post') as mocked_print_post:
            app.print_posts(blog)

            mocked_print_post.assert_called_with(blog.posts[0])

    def test_print_post(self):
        post = Post('Post title', 'Post content')
        expected_print = '''
--- Post title ---

Post content

'''
        with patch('builtins.print') as mocked_print:
            app.print_post(post)

            mocked_print.assert_called_with(expected_print)

    def test_ask_create_post(self):
        blog = Blog('Test', 'Test Author')
        app.blogs = {'Test': blog}
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Title', 'Test Content')

            app.ask_create_post()

            self.assertEqual(blog.posts[0].title, 'Test Title')
            self.assertEqual(blog.posts[0].content, 'Test Content')