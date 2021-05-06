#create a post class. properties: title and content.

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        pass

    def json(self):
        return {
            "title": self.title,
            "content": self.content,
        }
    def printpost(self):
        return (f"Titel: {self.title} \nInlägg: {self.content}")




