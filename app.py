from Member import Member
from Book import Book
from Collection import Collection
from JSONHandler import JSONHandler

memberHandler = JSONHandler("members.json")
bookHandler = JSONHandler("books.json")
collectionHandler = JSONHandler("collections.json")
dash = "--------------------------"

def collections():
    collections = []
    data = collectionHandler.read_data()
    for collection in data:
        collections.append(Collection(collection["id"],collection["name"],collection["books"]))
    return collections

def members():
    members = []
    data = memberHandler.read_data()
    for member in data:
        members.append(Member(member["name"],member["books"],member["id"],member["password"]))
    return members

def books():
    books = []
    data = bookHandler.read_data()
    for book in data:
        books.append(Book(book["id"],book["name"],book["author"],book["available"],book["usertags"]))
    return books

def loginUser():
        try:
            currentUser = {
                "id":input("Enter your id: "),
                "password":input("Enter your password: ")
            }
            for member in members():
                if currentUser["id"]==member.id and currentUser["password"]==member.password:
                    currentUser = member
                    print(f"Logged in successfully as {currentUser.name}")
                    return currentUser
        except:
            print("Wrong Credentials")
            currentUser = Member("","","","")
            currentUser.logOut()
            return currentUser

def register():
    dList = members()
    newMember = {
        "name": input("Enter your name: "),
        "books": [],
        "id": input("Create a unique Id: "),
        "password": input("Create a strong Password: ")
    }
    if dList == []:
        memberHandler.write_data(dList)
    memberHandler.add_entry(newMember)
    print(f"Welcome to the library {newMember['name']}!!")
    newMember = Member(newMember["name"],newMember["books"],newMember["id"],newMember["password"])
    return newMember

def searchBooks():
    inp = list(input(f"Search for a book\n{dash}\nWhat to search: ").split())
    booksFound = False
    print(dash)
    for term in inp:
        i = 1
        for b in books():
            for tag in b.tags:
                if term.lower() == tag.lower():
                    if not booksFound:
                        print("Books found:")
                    booksFound = True
                    print(f"\t{i}: {b.name}")
                    i+=1
                    break
    if not booksFound:
        print("Nothing matches your search")

def viewBooks():
    if len(books())==0:
        print("\nThis library is broke, please donate money so we can get books 🙏")
    else:
        avail = 0
        unavail = 0
        for b in books():
            if b.available:
                avail+=1
            elif not b.available:
                unavail+=1
        print(dash)
        if avail>=1:
            print("List of all available books:")
            for book in books():
                if book.available:
                    print(f"\t{book.id}: {book.name}\tAuthor: {book.author}")
        else:
            print("No books are available to borrow rn")
        print(dash)
        if unavail>=1:
            print("List of all borrowed books:")
            for book in books():
                if not book.available:
                    print(f"\t{book.id}: {book.name}\tAuthor: {book.author}")
        else:
            print("No books are borrowed rn")
        print(dash)
        print(f"Total books: {len(books())}")

def viewCollections():
    if len(collections())==0:
        print(f"{dash}\nNo collections are available atm\n{dash}")
    else:
        print(f"{dash}\nList of collections and their books:")
        for c in collections():
            print(f"{dash}\n{c.id}: {c.name}:")
            for b in c.books:
                for bb in books():
                    if b == bb.id:
                        print(f"\t{b}: {bb.name}")
            if len(c.books)==0:
                print("\tThis collection currently has no books")

def borrowBook(currentUser):
    l = 0
    for b in books():
        if b.available:
            l+=1
    if l ==0:
        print("There are no books available to borrow rn, try again later")
    else:
        print("List of available books: ")
        borrowList = []
        for book in books():
            if book.available:
                borrowList.append(book)
                print(f"[id: {book.id}]\t[name: {book.name}]")
        userSelection = input(f"{dash}\nEnter the id of the book you want to borrow: ")
        i = 0
        bookFound = False
        for b in books():
            for book in borrowList:
                if userSelection == book.id:
                    if book.id == b.id:
                        bookFound = True
                        j = 0
                        for m in members():
                            if m.id == currentUser.id:
                                m.books.insert(0,b.id)
                                bookHandler.update_data(i, "available", False)
                                memberHandler.update_data(j, "books", m.books)
                                print("You have borrowed the book, be sure to return it on time")
                                break
                            j+=1
                        break
                    i+=1
            if bookFound:
                break
        if not bookFound:
            print("Invalid Id")

def returnBook(currentUser):
    if len(currentUser.books)==0:
        print("You have no books to return")
    else:
        print("List of Your books: ")
        for b in currentUser.books:
            for bb in books():
                if b == bb.id:
                    print(f"[id: {bb.id}]\t[name: {bb.name}]")
        userSelection = input(f"{dash}\nEnter the id of the book you want to return: ")
        i = 0
        bookFound = False
        for b in currentUser.books:
            for bb in books():
                if b == userSelection:
                    if b == bb.id:
                        currentUser.books.remove(b)
                        bookFound = True
                        j = 0
                        for m in members():
                            if m.id == currentUser.id:
                                m.books.remove(b)
                                bookHandler.update_data(i, "available", True)
                                memberHandler.update_data(j, "books", m.books)
                                print("The book has successfully been returned")
                                break
                            j+=1
                        break
                    i+=1
                if bookFound:
                    break
        if not bookFound:
            print("Invalid Id")

def runApp():
    while True:
        inp = input(f"{dash}\nWhat would you like to do?\na: Login\nb: Register\n0: Exit\n{dash}\nEnter your choice: ")

        if inp == "a":
            print(f"Login\n{dash}")
            currentUser = loginUser()
            try:
                loggedIn = currentUser.loggedIn
            except:
                print("Invalid Credentials")
                loggedIn = False
            break
        elif inp == "b":
            print(f"Register\n{dash}")
            currentUser = register()
            loggedIn = currentUser.loggedIn
            break
        elif inp == "0":
            print(f"Come back again!\n{dash}")
            loggedIn = False
            break
    def user():
        for m in members():
            if m.id == currentUser.id:
                return m
    while loggedIn:
        currentUser = user()
            
        inp = input(f"{dash}\nwhat would you like to do?\na: view collections\nb: view books\nc: borrow a book\nd: return a book\ne: Search for a book\n0: Exit\n{dash}\nEnter your choice: ")

        if inp == "a":
            print(f"View collections")
            viewCollections()
        elif inp == "b":
            print(f"View books")
            viewBooks()
        elif inp == "c":
            print(f"Borrow a book\n{dash}")
            borrowBook(currentUser)
        elif inp == "d":
            print(f"Return a book\n{dash}")
            returnBook(currentUser)
        elif inp == "e":
            searchBooks()
        elif inp == '0':
            print(f"Come back again!\n{dash}")
            break

runApp()