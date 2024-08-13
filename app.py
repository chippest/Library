from Member import Member
from Book import Book
from JSONHandler import JSONHandler

memberHandler = JSONHandler("members.json")
bookHandler = JSONHandler("books.json")

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
        books.append(Book(book["id"],book["name"],book["author"],book["available"]))
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


def viewBooks():
    print("\nList of all available books:")
    for book in books():
        if book.available:
            print(f"\t{book.id}: {book.name}\tAuthor: {book.author}")
    print("\nList of all borrowed books:")
    for book in books():
        if not book.available:
            print(f"\t{book.id}: {book.name}\tAuthor: {book.author}")

def borrowBook():
    print("\nList of available books: ")
    borrowList = []
    for book in books():
        if book.available:
            borrowList.append(book)
            print(f"[id: {book.id}]\t[name: {book.name}]")
    userSelection = input("Enter the id of the book you want to borrow: ")
    i = 0
    bookFound = False
    for b in books():
        for book in borrowList:
            if userSelection == str(book.id):
                if book.id == b.id:
                    bookFound = True
                    j = 0
                    for m in members():
                        if m.id == currentUser.id:
                            m.books.insert(0,b.id)
                            bookHandler.update_data(i, "available", False)
                            memberHandler.update_data(j, "books", m.books)
                            break
                        j+=1
                    break
                i+=1
        if bookFound:
            break
    if not bookFound:
        print("Invalid Id")    

def returnBook():
    print("\nList of Your books: ")
    for b in currentUser.books:
        for bb in books():
            if b == bb.id:
                print(f"[id: {bb.id}]\t[name: {bb.name}]")
    userSelection = input("Enter the id of the book you want to borrow: ")
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
                            break
                        j+=1
                    break
                i+=1
            if bookFound:
                break
    if not bookFound:
        print("Invalid Id")


while True:
    inp = input("What would you like to do?\na: Login\nb: Register\nc: Exit\n\nEnter your choice: ")

    if inp == "a":
        currentUser = loginUser()
        try:
            loggedIn = currentUser.loggedIn
        except:
            print("Invalid Credentials")
            loggedIn = False
        break
    elif inp == "b":
        currentUser = register()
        loggedIn = currentUser.loggedIn
        break
    elif inp == "c":
        loggedIn = False
        break
def user():
    for m in members():
        if m.id == currentUser.id:
            return m
while loggedIn:
    currentUser = user()
        
    inp = input("\nwhat would you like to do?\na: view books\nb: borrow a book\nc: return a book\n0: Exit\n\nEnter your choice: ")

    if inp == "a":
        viewBooks()
    elif inp == "b":
        borrowBook()
    elif inp == "c":
        returnBook()
    elif inp == '0':
        break