from __future__ import annotations

from enum import Enum
from random import randint, choice
from abc import ABC, abstractmethod

# Random bounds
MIN_PAGE = 100
MAX_PAGE = 1000
MIN_BOOK = 1
MAX_BOOK = 1


# Enum class for Genre: genre can only ba among a predefined list
class Genre(Enum):
    DEFAULT = "Default"
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    MYSTERY = "Mystery"
    FANTASY = "Fantasy"
    SCIFI = "Science Fiction"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    COMEDY = "Comedy"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    CHILDREN = "Children"
    ADVENTURE = "Adventure"


#####################################################################
#####################   SINGLETON METACLASS    ######################
##   Singleton Paradigm, only one instance of the class can exist  ##
##    A call to creation MyClass() will either create an object    ##
##                    Or return the existing one                   ##
##   You are not supposed to know this code, only that it exists   ##
##    Singleton metaclass is very generic, can be found online     ##
##             Should be adapted if any parameters needed          ##
#####################################################################

### Singleton
### The Library could be a singleton and must only inherit from this
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#####################################################################
#####################  EVENT-BASED PROGRAMING  ######################
### When a Generator create an Event, it must notify the listener ###
######## Listener must register themselves to the Generator  ########
#### Create generic (abstract) class for listeners and generator ####
######## Actual classes must inherit from the generic class  ########
## and implement abstract methods (and overwrite others if needed) ##
#####################################################################

### Abstract classes only needed to centralize the concept of sources
class Generator:
    pass

class Event:
    def __init__(self, source: Generator) -> None:
        self.source = source

### BookEvent
### Generator: Writer
### Listener: User & Library
### Event: BookEvent
class BookEventGenerator(Generator):
    def __init__(self):
        self.list_bookEventListener = list()


    def unregisterListener(self, listener):
        self.unregisterBookListener(listener)

    def registerBookListener(self, listener: BookEventListener) -> None:
        if listener not in self.list_bookEventListener:
            self.list_bookEventListener.append(listener)
            print(f"{listener.name} has been registered to book events.")

    def unregisterBookListener(self, listener: BookEventListener) -> None:
        if listener in self.list_bookEventListener:
            self.list_bookEventListener.remove(listener)
            print(f"{listener.name} has been unregistered from book events.")

    def createBookEvent(self, title: str, authors: list['Writer']) -> 'BookEvent':
        return BookEvent(self, title, set(authors))


class BookEventListener:
    def bookEventNotice(self, book_event: BookEvent) -> None:
        print(f"{self.name} has been notified about a new book event: {book_event.title}")

    def follow(self, generator: BookEventGenerator) -> None:
        generator.registerBookListener(self)



class BookEvent(Event):
    def __init__(self, source: BookEventGenerator, title: str, authors: set[Writer] = None) -> None:
        super(BookEvent, self).__init__(source)
        self.title: str = title
        self.authors = authors

    def __repr__(self) -> str:
        return f"[{type(self).__name__}] {self.title}"


### availableEvent
###### Generator: Library
###### Listener: User
###### Event: availableEvent
class AvailableEventGenerator(Generator):
    def __init__(self):
        self.list_bookEventListener = list()

    def registerAvailableListener(self, listener: BookEventListener) -> None:
        if listener not in self.list_bookEventListener:
            self.list_bookEventListener.append(listener)
            print(f"{listener.name} has been registered to available events.")

    def unregisterAvailableListener(self, listener: BookEventListener) -> None:
        if listener in self.list_bookEventListener:
            self.list_bookEventListener.remove(listener)
            print(f"{listener.name} has been unregistered from available events.")

    def createAvailableEvent(self, title:str) -> None:
        return AvailableEvent(self, title)

class AvailableEventListener:
    def availableEventNotice(self, available: AvailableEvent):
        print(f"{self.name} has been notified about a new available book: {available.title}")

class AvailableEvent(Event):
    def __init__(self, source: AvailableEventGenerator, title: str) -> None:
        super(AvailableEvent, self).__init__(source)
        self.title = title

    def __repr__(self) -> str:
        return f"[{type(self).__name__}] {self.title} should be available)"

#####################################################################
####################           PROGRAM          #####################
## __ denote "private" field: those can't be use outside of class  ##
#####################################################################
class Library(BookEventListener, AvailableEventGenerator, metaclass=Singleton):
    def __init__(self):
        super(Library, self).__init__()
        self.name = "Library of Ena-shine"
        self.__registered: set[User] = set()
        self.__available: dict[Book, int] = dict()
        self.__followed: set[BookEventGenerator] = set()
        self.__reserved: dict[str, list[AvailableEventListener]] = dict()
        self.__followers: set[AvailableEventListener] = set()

    def __repr__(self):
        return f"[{type(self).__name__}] {self.name}."

    # To Do: add a book in stock. If the book title is in the "reserved" dict, create the associated availableEvent
    def __addBook(self, book: Book, qte: int = 1) -> None:
        if book not in self.__available:
            self.__available[book] = qte
            # Check if the book is reserved
            if book.title in self.__reserved:
                for listener in self.__reserved[book.title]:
                    available_event = self.createAvailableEvent(book.title)
                    listener.availableEventNotice(available_event)
                del self.__reserved[book.title]
        else:
            self.__available[book] += qte
            # Notify all followers about the increased availability
            for listener in self.__followers:
                available_event = self.createAvailableEvent(book.title)
                listener.availableEventNotice(available_event)

    # To Do: remove a book from stock, if the book is not in stock, do nothing
    def __removeBook(self, book: Book) -> None:
        if book in self.__available:
            del self.__available[book]
            print(f"{book.title} has been removed from the library.")
        else:
            print(f"{book.title} is not available in the library.")

    # ToDo: register and unregister users 
    def register(self, user: User) -> None:
        self.__registered.add(user)
        print(f"{user.name} has been registered to the library.")

    def unregister(self, user: User) -> None:
        self.__registered.discard(user)
        print(f"{user.name} has been unregistered from the library.")

    def getRegistered(self) -> set[User]:
        return self.__registered

    def follow(self, writer: BookEventGenerator) -> None:
        self.__followed.add(writer)
        writer.registerBookListener(self)

    # Get notified by a writer that a book has been writen
    # If interested, add the book in a random quantity
    # Several approach are possible, sets have a method setA.intersection(setB)
    # This methods return A inter B (that you can cast as a list)
    def bookEventNotice(self, book_event: BookEvent) -> None:
        print(f"{self.name} has been notified about a new book event: {book_event.title}")
        # Check if the book is already in stock
        for book in self.__available:
            if book.title == book_event.title:
                print(f"{book_event.title} is already in stock.")
                return
        
        # If not, add the book to stock with a random quantity
        quantity = randint(MIN_BOOK, MAX_BOOK)
        new_book = Book(book_event.title, genres={Genre.DEFAULT}, nb_pages=randint(MIN_PAGE, MAX_PAGE), authors=book_event.authors)
        self.__addBook(new_book, quantity)

    # Create the available event when a book is added, this event will be used to notice listener
    def createAvailableEvent(self, title) -> AvailableEvent:
        return AvailableEvent(title)

    def getFollowed(self) -> set[BookEventGenerator] :
        return self.__followed

    def consult(self, user: User) -> list[str]:
        if user not in self.__registered:
            print(f"{user.name} is not registered in the library.")
            return []
        print(f"{user.name} is consulting the library.")
        # Return a list of titles of available books
        return [book.title for book, quantity in self.__available.items() if quantity > 0]

    def getStock(self) -> dict[Book, int]:
        return self.__available

    def getReservation(self) -> dict[str, list[AvailableEventListener]]:
        return self.__reserved

    # The user must be registered and allowed to borrow book
    # Find the book by the name (use a Proxy) and give that book to the user
    # Will add the title in __reserved if not available
    # -> BookEvent|None : return a BookEvent or None
    def requestBook(self, title: str, user: User) -> Book | None:
        if user not in self.__registered:
            print(f"{user.name} is not registered in the library.")
            return None
        
        # Check if the book is available
        for book, quantity in self.__available.items():
            if book.title == title and quantity > 0:
                # Decrease the quantity of the book
                self.__available[book] -= 1
                if self.__available[book] == 0:
                    self.__removeBook(book)
                return book
        
        # If the book is not available, add it to reserved
        if title not in self.__reserved:
            self.__reserved[title] = []
        if user not in self.__reserved[title]:
            self.__reserved[title].append(user)
            print(f"{title} is not available, {user.name} has been added to the reservation list.")
        else :
            print(f"{user.name} is already on the reservation list for {title}.")
        return None
    
    # ToDo
    def returnBook(self, book: Book) -> None:
        if book in self.__available:
            self.__available[book] += 1
            print(f"{book.title} has been returned to the library.")

class Book:
    def __init__(self, title: str, genres: set[Genre], nb_pages: int,
                 authors: set[Writer] = None) -> None:
        self.title: str = title
        self.nb_pages: int = nb_pages
        self.genres = genres
        self.authors = authors

    def __repr__(self) -> str:
        return f"[{type(self).__name__}] {self.title} ({self.nb_pages} pages), written by {self.getListAuthorsName()}"

    def __eq__(self, other: Book) -> bool:
        if isinstance(other, Book):
            return self.title == other.title
        return False

    # Necessary for set and such, just copy/paste from the internet
    def __hash__(self):
        return hash(self.title)

    def getListAuthorsName(self) -> list[str]:
        return [author.name for author in self.authors]

    # Add an author to the book
    def addAuthor(self, author: Writer) -> None:
        if self.authors is None:
            self.authors = set()
        elif not isinstance(self.authors, set):
            raise TypeError("Authors must be a set of Writer instances")
        if author not in self.authors:
            self.authors.add(author) 

    # ToDo: must check if the book has the given title
    def hasTitle(self, title: str) -> bool:
        return self.title == title

class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"[{type(self).__name__}] {self.name} ({self.age} years old)"

class Writer(Person, BookEventGenerator):
    def __init__(self, name: str, age: int) -> None:
        super(Writer, self).__init__(name, age)
        BookEventGenerator.__init__(self)
        self.written = set()
        self.__followers: set[BookEventListener] = set()

    # ToDo: should create a Book with title, nb_pages, genres, coauthor and add self as author. Once done, must notify the Library about creation
    # Adding a coauthor in the book should trigger the Book event from associated author!
    def write(self, title: str, nb_pages: int = randint(MIN_PAGE, MAX_PAGE), genres=None,
                        coauthor: set['Writer'] = None) -> 'Book':
        if coauthor is None:
            coauthor = set()
        book = Book(title, genres or {Genre.DEFAULT}, nb_pages, authors={self} | coauthor)
        if book not in self.written:
            self.written.add(book)
            for author in coauthor:
                if author != self:
                    author.written.add(book)
            book_event = self.createBookEvent(title, coauthor)
            Library().bookEventNotice(book_event)
            Library()._Library__addBook(book)
            # Notify all followers about the new book
            for follower in self.__followers:
                follower.bookEventNotice(book_event)
        else:
            print(f"{self.name} has already written {book.title}, not creating a new event.")
        return book

    # Create a BookEvent with title and all authors (self + coauthors)
    def createBookEvent(self, title: str, coauthor: set['Writer'] = None) -> 'BookEvent':
        if coauthor is None:
            coauthor = set()
        authors = {self} | coauthor
        return BookEvent(self, title, authors)

    # must order a book if the book is not already written
    def orderBook(self, book_event: BookEvent) -> Book|None:
        library = Library()
        title = book_event.title
        for book, quantity in library.getStock().items():
            if book.title == title and quantity > 0:
                return book
        return None

    # register followers to the writer
    def getFollowers(self) -> list[BookEventListener]:
        return list(self.__followers)

class User(Person, BookEventListener, AvailableEventListener):
    def __init__(self, name: str, age: int) -> None:
        super(User, self).__init__(name, age)
        self.read:list[Book] = []
        # __attributes: "private", can not be accessed by anything else
        self.__borrowed:list[Book] = []

    def readBook(self, book: Book):
        if book not in self.read:
            self.read.append(book)
        else:
            print(f"{self.name} has already read {book.title}, not adding it again.")

    def listTitleRead(self) -> list[str]:
        return [book.title for book in self.read]

    def follow(self, writer: BookEventGenerator) -> None:
        writer.registerBookListener(self)

    # ToDo: Must borrow a book from the library with following algo
    # 1 get the titles of available books
    # 2: Select a random titles among them, using randint or choice
    # 3: Ask to the library for the Book
    # 4: Wait for the book in another method
    def borrow(self, title:str) -> None:
        found = False
        for book in Library().getStock():
            if book.title == title:
                found = True
                result = Library().requestBook(title, self)
                if result:
                    self.__borrowed.append(result)
                    print(f"{self.name} borrowed {result.title}.")
                else:
                    print(f"{title} is not available for borrowing.")
                break
        if not found:
            print(f"{title} is not in the library's stock.")

    def borrowRandomBook(self) -> None:
        available_books = [book for book in Library().getStock() if book not in self.__borrowed]
        if available_books:
            book = choice(available_books)
            self.borrow(book.title)
        else:
            print(f"{self.name} has already borrowed all available books.")

    # ToDo: must return a book, algo of your choice
    def returnBook(self, book: Book) -> None:
        if book in self.__borrowed:
            self.__borrowed.remove(book)
            Library().returnBook(book)
        else:
            print(f"{book.title} is not borrowed by {self.name}.")

    def nbBorrowed(self) -> int:
        return len(self.__borrowed)

# Ptit observer des livres
    def bookEventNotice(self, book_event:BookEvent) -> None:
        print(f"{self.name} has been notified about a new book event: {book_event.title}")

    def availableEventNotice(self, available: AvailableEvent):
        print(f"{self.name} has been notified about a new available book: {available.title}")
