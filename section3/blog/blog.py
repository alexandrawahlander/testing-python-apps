from post import Post
#arguments: title, author. properties: title, author, posts
class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.posts = []

    def __repr__(self):
        return f"{self.title} by {self.author} ({(str(len(self.posts)))} post{'s' if len(self.posts) != 1 else ''})"

    def json(self):
        return{
            "Title": self.title,
            "Author": self.author,
            "Posts": [post.json() for post in self.posts]
        }

    def create_post(self, title, content):
        self.posts.append(Post(title, content))


