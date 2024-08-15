from Member import Member
from Book import Book
from Collection import Collection
from JSONHandler import JSONHandler
import random

adminHandler = JSONHandler("admin.json")
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

def createBook():
    dList = books()
    bookIds = []
    for b in dList:
        bookIds.append(b.id)
    while True:
        rand = str(random.randint(1000, 9999))
        if rand not in bookIds:
            print(f"Create a new book\n{dash}\nBook's new ID: {rand}")
            break
    newBook = {
        "id": rand,
        "name": input("Enter book's name: "),
        "author": input("Enter authors name: "),
        "available": True,
        "usertags": list(input("Enter tags for the book, seperated by a space, leave empty for no tags: ").split())
    }
    if dList == []:
        bookHandler.write_data(dList)
    bookHandler.add_entry(newBook)
    print(f"\nThe book [{newBook['name']}] has been added!")

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
                    for member in members():
                        for mbook in member.books:
                            if mbook == book.id:
                                print(f"\t{book.id}: {book.name}\tAuthor: {book.author}\tBorrowed by: {member.name}")
        else:
            print("No books are borrowed rn")
        print(dash)
        print(f"Total books: {len(books())}")

def deleteBook():
    if len(books())==0:
        print(f"{dash}\nThere are no books to be deleted")
    else:
        print(f"Delete a books")
        viewBooks()
        inp = input(f"{dash}\nEnter id of book to delete: ")
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
                print(f"\nThe book \"{b.name}\" has been removed from the library")
                k = 0
                for c in collections():
                    for bb in c.books:
                        if bb == b.id:
                            c.books.remove(b.id)
                            collectionHandler.update_data(k, "books", c.books)
                            print(f"Book has been removed form [{c.name}] collection")
                    k+=1
                            
                break
            i+=1
        if invalidInput:
            print("\nInvalid Id")

def updateBook():
    if len(books())==0:
        print(f"{dash}\nThere are no books to update")
    else:
        print(f"Update a book")
        viewBooks()
        inp = input("Enter id of book to update: ")
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
                print(f"\nThe book \"{b.name}\" has been updated")
                break
            i+=1
        if invalidInput:
            print("\nInvalid Id")

def register():
    dList = members()
    print(f"Create new user\n{dash}")
    newMember = {
        "name": input("Enter your name: "),
        "books": [],
        "id": input("Create a unique Id: "),
        "password": input("Create a strong Password: ")
    }
    if dList == []:
        memberHandler.write_data(dList)
    memberHandler.add_entry(newMember)
    print(f"\nUser {newMember['name']} has been added")

def viewUsers():
    if len(members())==0:
        print(f"{dash}\nThere are no members in this useless library")
    else:
        print(f"List of all members:")
        print(dash)
        for member in members():
            print(f"[id]: {member.id}\n[name]: {member.name}")
            print(f"[Books]:")
            if len(member.books)==0:
                print("\tUser has no books")
            else:
                bNum = 1
                for book in member.books:

                    for bookid in books():
                        if book == bookid.id:
                            print(f"\t{bNum}: {bookid.name}, by {bookid.author}")
                    
                    bNum+=1
            print(dash)
        print(f"Total members: {len(members())}")

def deleteUser():
    if  len(members())==0:
        print(f"{dash}\nThere are no members to delete")
    else:
        print(f"Delete a user\n{dash}")
        viewUsers()
        inp = input(f"{dash}\nEnter id of member to delete: ")
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
                print(f"\nUser \"{m.name}\" has been deleted")
                if hadBooks:
                    print(f"the users books have successfully been retireved")
                break
            j+=1
        if invalidInput:
            print("\nInvalid Id")

def updateUser():
    if len(members())==0:
        print(f"{dash}\nThere are no members to update in this useless library")
    else:
        print(f"Update a user\n{dash}")
        viewUsers()
        inp = input(f"{dash}\nEnter id of member to update: ")
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
                print(f"\nUser \"{m.name}\" has been updated")
                break
            j+=1
        if invalidInput:
            print("\nInvalid Id")

def createCollection():
    dlist = collections()
    colIds = []
    for c in dlist:
        colIds.append(c.id)
    while True:
        rand = str(random.randint(1000, 9999))
        if rand not in colIds:
            print(f"Create a new collection\n{dash}\nNew collections ID: {rand}")
            break
    newCollection = {
        "id": rand,
        "name":input("Enter collections name: "),
        "books":[]
    }
    if dlist == []:
        collectionHandler.write_data(dlist)
    collectionHandler.add_entry(newCollection)
    print(f"\nThe collection [{newCollection['name']}] has been created!")

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

def collectionAdd():
    if len(collections())==0:
        print("\nThere are no collections to add books to")
    else:
        if len(books())==0:
            print("\nThere are no books to add to a collection")
        else:
            viewBooks()
            bk = input(f"{dash}\nEnter id of book you want to add to a collection: ")
            bookFound = False
            for b in books():
                if b.id == bk:
                    bookFound = True
                    viewCollections()
                    col = input(f"{dash}\nEnter id of collection you would like to add {b.name} to: ")
                    colFound = False
                    j = 0
                    for c in collections():
                        if c.id == col:
                            colFound = True
                            if b.id not in c.books:
                                c.books.insert(0, b.id)
                                collectionHandler.update_data(j, "books", c.books)
                                print("\nBook successfully added to collection")
                            else:
                                print("\nBook already in collection")
                        j+=1
            if not bookFound or not colFound:
                print("\nInvalid Id")

def collectionRemove():
    if len(collections())==0:
        print("\nThere are no collections to remove books from")
    else:
        if len(books())==0:
            print("\nThere are no books to remove from a collection")
        else:
            print("Remove a book from collection")
            viewCollections()
            col = input(f"{dash}\nEnter id of collection you want to remove a book from: ")
            colFound = False
            j = 0
            for c in collections():
                if c.id == col:
                    if len(c.books)==0:
                        print("\nThere are no books in this collection")
                    else:
                        colFound = True
                        print(f"{dash}\nList of books in collection:\n{dash}")
                        for bb in c.books:
                            for bbb in books():
                                if bb == bbb.id:
                                    print(f"{bbb.id}: {bbb.name}")
                        bk = input(f"{dash}\nEnter id of book you want to remove: ")
                        bookFound = False
                        for b in books():
                            if b.id == bk and b.id in c.books:
                                bookFound = True
                                c.books.remove(b.id)
                                collectionHandler.update_data(j, "books", c.books)
                                print("\nBook successfully removed from collection")
                        if not bookFound:
                            print("\nInvalid book id")
                j+=1
            if not colFound:
                print("\nInvalid Id")

def updateCollection():
    if len(collections())==0:
        print(f"{dash}\nThere are no collections to update")
    else:
        viewCollections()
        inp = input(f"{dash}\nEnter id of collection to update: ")
        k = 0
        invalidInput = True
        for c in collections():
            if inp == c.id:
                invalidInput = False
                newName = input("Enter new name for collection: ")
                collectionHandler.update_data(k, "name", newName)
                print("The collection has been updated!")
                break
            k+=1
        if invalidInput:
            print("Invalid Id") 

def deleteCollection():
    if len(collections())==0:
        print(f"{dash}\nThere are no collections to delete in this useless library")
    else:
        viewCollections()
        inp = input(f"{dash}\nEnter id of collection to delete permanently: ")
        invalidInput = True
        k = 0
        for c in collections():
            if inp == c.id:
                invalidInput = False
                collectionHandler.remove_entry(k)
                print(f"Collection [{c.name}] has successfully been removed!")
            k+=1
        if invalidInput:
            print("Invalid Id")

def admin():
    loggedIn = False
    id = input(f"{dash}\nEnter your admin id: ")
    password = input("Enter your admin password: ")
    for admin in adminHandler.read_data():
        if id == admin["id"] and password == admin["password"]:
            loggedIn = True
            print(f"{dash}\nAdmin login successfull")
            while True:
                inp = input(f"{dash}\nWhat would you like to modify, sir?\na: Modify Members\nb: Modify Books\nc: Modify Collections\n0: Exit\n{dash}\nEnter your choice: ")
                while True:
                    if inp == "a":
                        adminCommand = input(f"{dash}\nSelect a command:\na: View members\nb: Register a new member\nc: Delete a member\nd: Update a memeber\n0: Exit\n{dash}\nEnter your choice: ")
                        match adminCommand:
                            case "a":
                                viewUsers()
                            case "b":
                                register()
                            case "c":
                                deleteUser()
                            case "d":
                                updateUser()
                            case "0":
                                break
                            case "":
                                print("Invalid command")
                    elif inp =="b":
                        adminCommand = input(f"{dash}\nSelect a command:\na: View Books\nb: Add a book\nc: Remove a book\nd: Update a book\n0: Exit\n{dash}\nEnter your choice: ")
                        match adminCommand:
                            case "a":
                                viewBooks()
                            case "b":
                                createBook()
                            case "c":
                                deleteBook()
                            case "d":
                                updateBook()
                            case "0":
                                break
                            case "":
                                print("Invalid command")
                    elif inp == "c":
                        adminCommand = input(f"{dash}\nSelect a command:\na: View collections\nb: Add a book to collection\nc: Remove a book from collection\nd: Create a new collection\ne: Update an existing collection\nf: Delete an existing collection\n0: Exit\n{dash}\nEnter your choice: ")
                        match adminCommand:
                            case "a":
                                viewCollections()
                            case "b":
                                collectionAdd()
                            case "c":
                                collectionRemove()
                            case "d":
                                createCollection()
                            case "e":
                                updateCollection()
                            case "f":
                                deleteCollection()
                            case "0":
                                break
                            case "":
                                print("Invalid command")
                    elif inp == "0":
                        break
                    else:
                        print("\nInvalid Command")
                        break
                if inp == "0":
                    print(f"Return again! ciao\n{dash}")
                    break
    if not loggedIn:
        print(f"\nWrong Credentials\n{dash}")

admin()