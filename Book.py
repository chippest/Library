class Book:
    def __init__(self, id, name, author, available, userTags) -> None:
        self.id = id
        self.name = name
        self.author = author
        self.available = available
        self.usertags = userTags
        self.tags = self.usertags + self.name.split() + self.author.split() + self.id.split()
    def borrowBook(self):
        self.available = False
    def returnBook(self):
        self.available = True