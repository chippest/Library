class Book:
    def __init__(self, id, name, author, available) -> None:
        self.id = id
        self.name = name
        self.author = author
        self.available = available
    def borrowBook(self):
        self.available = False
    def returnBook(self):
        self.available = True