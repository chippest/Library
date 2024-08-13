from Member import Member
from Book import Book
from JSONHandler import JSONHandler
import random

adminHandler = JSONHandler("admin.json")
memberHandler = JSONHandler("members.json")
bookHandler = JSONHandler("books.json")
dash = "--------------------------"

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

def createBook():
    dList = books()
    bookIds = []
    for b in dList:
        bookIds.append(b.id)
    while True:
        rand = str(random.randint(1000, 9999))
        if rand not in bookIds:
            print(f"Book's new ID: {rand}")
            break
    newBook = {
        "id": rand,
        "name": input("Enter book's name: "),
        "author": input("Enter authors name: "),
        "available": True
    }
    if dList == []:
        bookHandler.write_data(dList)
    bookHandler.add_entry(newBook)

def viewBooks():
    print("\nList of all available books:")
    for book in books():
        if book.available:
            print(f"\t{book.id}: {book.name}\tAuthor: {book.author}")
    print("\nList of all borrowed books:")
    for book in books():
        if not book.available:
            for member in members():
                for mbook in member.books:
                    if mbook == book.id:
                        print(f"\t{book.id}: {book.name}\tAuthor: {book.author}\tBorrowed by: {member.name}")

def viewMembers():
    print("List of all members:")
    for member in members():
        print(dash)
        print(f"[id]: {member.id}\n[name]: {member.name}")
        if member.books != []:
            print(f"[Books]:")
            bNum = 1
            for book in member.books:

                for bookid in books():
                    if book == bookid.id:
                        print(f"\t{bNum}: {bookid.name}, by {bookid.author}")
                
                bNum+=1

def deleteUser():
    viewMembers()
    inp = input("\nEnter id of member to delete: ")
    j = 0
    invalidInput = True
    hadBooks = False
    for m in members():
        if inp == m.id:
            invalidInput = False
            i = 0
            for bb in books():
                for b in m.books:
                    if b == bb.id:
                        bookHandler.update_data(i, "available", True)
                        hadBooks = True
                i+=1
            memberHandler.remove_entry(j)
            print(f"User \"{m.name}\" has been deleted")
            if hadBooks:
                print(f"the users books have successfully been retireved")
            break
        j+=1
    if invalidInput:
        print("Invalid Id")

def deleteBook():
    viewBooks()
    inp = input("\nEnter id of book to delete: ")
    i = 0
    invalidInput = True
    for b in books():
        if inp == b.id:
            invalidInput = False
            j = 0
            for m in members():
                for bb in m.books:
                    if bb == b.id:
                        m.books.remove(b.id)
                        memberHandler.update_data(j, "books", m.books)
                j+=1
            bookHandler.remove_entry(i)
            print(f"The book \"{b.name}\" has been removed from the library")
            break
        i+=1
    if invalidInput:
        print("Invalid Id")

def updateUser():
    viewMembers()
    inp = input("\nEnter id of member to update: ")
    j = 0
    invalidInput = True
    for m in members():
        if inp == m.id:
            invalidInput = False
            editedUser = {
                "name":input("Enter a new name: "),
                "books": m.books,
                "id":input("Enter a new ID: "),
                "password":input("Enter a new password: ")
            }
            memberHandler.update_data(j, "name", editedUser["name"])
            memberHandler.update_data(j, "books", editedUser["books"])
            memberHandler.update_data(j, "id", editedUser["id"])
            memberHandler.update_data(j, "password", editedUser["password"])
            print(f"User \"{m.name}\" has been updated")
            break
        j+=1
    if invalidInput:
        print("Invalid Id")

def updateBook():
    viewBooks()
    inp = input("\nEnter id of book to update: ")
    i = 0
    invalidInput = True
    for b in books():
        if inp == b.id:
            invalidInput = False
            editedBook = {
                "name":input("Enter a new name: "),
                "author":input("Enter a new author: ")
            }
            bookHandler.update_data(i, "name", editedBook["name"])
            bookHandler.update_data(i, "author", editedBook["author"])
            print(f"The book \"{b.name}\" has been updated")
            break
        i+=1
    if invalidInput:
        print("Invalid Id")

def admin():
    loggedIn = False
    id = input("Enter your admin id: ")
    password = input("Enter your admin password: ")
    for admin in adminHandler.read_data():
        if id == admin["id"] and password == admin["password"]:
            loggedIn = True
            print("logged in")
            while True:
                inp = input("\nWhat would you like to do?\na: View members\nb: Delete a member\nc: Update a memeber\nd: View Books\ne: Add a book\nf: Remove a book\ng: Update a book\n0: Exit\n\nEnter your choice: ")
                match inp:
                    case "a":
                        viewMembers()
                    case "b":
                        deleteUser()
                    case "c":
                        updateUser()
                    case "d":
                        viewBooks()
                    case "e":
                        createBook()
                    case "f":
                        deleteBook()
                    case "g":
                        updateBook()
                    case "0":
                        break
    if not loggedIn:
        print("Wrong Credentials")
admin()