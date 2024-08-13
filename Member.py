class Member:
    def __init__(self, name, books, id, password) -> None:
        self.name = name
        self.books = books
        self.id = id
        self.password = password
        self.loggedIn = True
    def logOut(self):
        self.loggedIn = False